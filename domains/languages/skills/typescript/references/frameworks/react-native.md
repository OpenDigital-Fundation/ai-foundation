# TypeScript and JavaScript — react-native

Part of `languages:typescript`. Load only when the project uses react-native.

## React Native / Expo Coding Style

<!-- source: affaan-m/ECC rules/react-native/coding-style.md -->

> This file extends common/coding-style.md with React Native / Expo specific content.

### Components

- Define props with a named `interface` or `type`; do not use `React.FC`.
- Keep screens thin: a screen composes hooks + presentational components, it does not hold heavy logic.
- One component per file for anything reusable; co-locate small private subcomponents.
- Prefer function components and hooks. No class components.

```tsx
interface AvatarProps {
  uri: string
  size?: number
  onPress?: () => void
}

export function Avatar({ uri, size = 40, onPress }: AvatarProps) {
  return (
    <Pressable onPress={onPress}>
      <Image source={{ uri }} style={{ width: size, height: size, borderRadius: size / 2 }} />
    </Pressable>
  )
}
```

### Styling

Pick ONE styling system per project and stay consistent. `StyleSheet.create()` is the framework-native option; utility-class libraries (e.g. NativeWind) are a common alternative. This rule is library-agnostic — what matters is consistency and avoiding inline allocations.

- StyleSheet: define styles with `StyleSheet.create()` at module scope — never build style objects inline inside `render`/JSX on hot paths (it allocates on every render).
- Utility-class approach: extract repeated class strings into shared constants or a variant helper.
- Never hardcode raw colors, spacing, or font sizes scattered across files. Centralize design tokens (theme file or config).

```tsx
// WRONG: inline style object recreated every render
<View style={{ padding: 16, backgroundColor: '#fff' }} />

// CORRECT (StyleSheet)
const styles = StyleSheet.create({ card: { padding: 16, backgroundColor: '#fff' } })
<View style={styles.card} />

// CORRECT (NativeWind)
<View className="p-4 bg-white" />
```

### Platform Differences

- Use platform-specific files (`Component.ios.tsx`, `Component.android.tsx`) for substantial divergence.
- Use `Platform.select()` / `Platform.OS` for small differences only.
- Account for safe areas with `react-native-safe-area-context`; do not hardcode status bar / notch offsets.

### Imports & Project Layout

- Use the Expo/TS path alias (e.g. `@/components/...`) instead of long relative chains.
- Organize by feature/domain, not by type. Keep files focused (200-400 lines typical, 800 max).

### Logging

- No `console.log` in shipped code. Use a logger and strip logs in production builds.
- Surface user-facing errors through UI state, not console.

### TypeScript

All TypeScript rules from `rules/typescript/` apply (explicit types on public APIs, avoid `any`, Zod for validation, immutable updates). This file only adds RN-specific guidance on top.

## React Native / Expo Patterns

<!-- source: affaan-m/ECC rules/react-native/patterns.md -->

> This file extends common/patterns.md with React Native / Expo specific patterns.
> Note: Do NOT install the `web/` ruleset in a React Native project — those patterns assume the DOM (e.g. URL-as-state) and do not apply here.

### Navigation (Expo Router)

Expo Router is Expo's built-in, file-based router (`app/` directory); React Navigation is the established alternative. The examples below use Expo Router; the principles apply either way.

- Keep route files (`app/**`) thin — they wire params + hooks to a screen component that lives in `components/` or `features/`.
- Type route params; validate untrusted params (e.g. from deep links) with Zod before use.
- Use typed navigation helpers (`useLocalSearchParams`, `Link`, `router.push`).
- Centralize linking config; never trust deep-link params without validation.

```tsx
// app/user/[id].tsx
import { useLocalSearchParams, router } from 'expo-router'
import { z } from 'zod'

const Params = z.object({ id: z.string().uuid() })

export default function UserScreen() {
  // Use safeParse, not parse: a malformed deep link would otherwise throw
  // during render and crash the screen. Redirect instead of throwing.
  const parsed = Params.safeParse(useLocalSearchParams())
  if (!parsed.success) {
    router.replace('/not-found')
    return null
  }
  return <UserProfile userId={parsed.data.id} />
}
```

### State Management

The rule is to keep these concerns separate and not duplicate server data into client stores. The tools listed are common choices, not requirements — pick what fits your project.

| Concern | Common choices |
|---------|---------|
| Server state | a server-cache library (TanStack Query, SWR) |
| Client/UI state | a lightweight store (Zustand, Jotai) or Context |
| Navigation/route state | Expo Router params (NOT a global store) |
| Form state | a form library (e.g. React Hook Form) with schema validation |
| Secure persistence | `expo-secure-store` |
| Non-secure persistence | `AsyncStorage` / MMKV |

- Derive values instead of storing redundant computed state.
- Keep global client state minimal; prefer local `useState` until sharing is actually needed.

### Data Fetching

Use a server-cache library (TanStack Query, SWR) instead of ad-hoc fetch-in-`useEffect`. The examples use TanStack Query.

- Route server reads through the cache (e.g. `useQuery`) and mutations through it (e.g. `useMutation`) with cache invalidation.
- Validate API responses with Zod at the boundary; infer types from the schema. (Zod is already the validation default in this pack's TypeScript standards.)
- Handle the three states explicitly in UI: loading, error, empty.
- Use optimistic updates for fast interactions: snapshot, apply, roll back on failure with visible feedback.
- Fetch independent data in parallel; avoid request waterfalls between parent and child.

```tsx
function useUser(id: string) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: async () => userSchema.parse(await api.getUser(id)),
  })
}
```

### Lists

- Use `FlatList`/`SectionList` (or `FlashList` for large/heavy lists) — never `.map()` a large array inside a `ScrollView`.
- Provide a stable `keyExtractor`; memoize `renderItem`.
- Paginate or virtualize long data sets.

### Custom Hooks

- Extract reusable logic (data, permissions, device APIs) into `use*` hooks.
- Keep side effects (Expo SDK calls, subscriptions) inside hooks, not in JSX.

### Async & Effects

- Clean up subscriptions, timers, and listeners in the effect's return function.
- Cancel or ignore stale async results on unmount to avoid setState-after-unmount.

## React Native / Expo Patterns

<!-- source: affaan-m/ECC pi/core/skills/react-native-patterns/SKILL.md -->

Practical patterns for building production React Native apps with Expo. Covers navigation, state, data fetching, lists, styling, and native APIs. Pairs with the `rules/react-native/` ruleset: rules say *what* to enforce, this skill shows *how*.

Libraries named below (NativeWind, Zustand/Jotai, TanStack Query) are common, well-established options shown for illustration — the patterns matter more than the specific package, and any equivalent works. Zod is used for validation to stay consistent with this pack's TypeScript standards.

These patterns assume the managed Expo workflow (Expo Router, EAS, `expo-*` modules) on the New Architecture (the default in recent Expo SDKs, mandatory from SDK 55+). They do NOT assume the browser DOM — React Native has no `<div>`, no URL bar, and no web data-fetching defaults.

### When to Activate

Use this skill when:

- Building or editing React Native / Expo screens, components, or navigation
- Setting up routing with Expo Router (file-based `app/` directory)
- Deciding where state belongs (server cache vs client store vs route params vs form)
- Wiring data fetching with TanStack Query and validating responses with Zod
- Rendering long or heavy lists
- Choosing or applying a styling approach (NativeWind or StyleSheet)
- Accessing native device APIs (camera, location, notifications) or secure storage
- Reviewing RN code for mobile-specific issues

Do NOT use the web/React-DOM patterns here — URL-as-state, `<div>`, and SWR-for-browser do not apply to React Native.

### Core Concepts

#### Project structure (Expo Router)

File-based routing under `app/`. Keep route files thin: they read and validate params, then delegate to a screen component that lives in `components/` or `features/`.

```
app/
  _layout.tsx          # root stack
  (tabs)/
    _layout.tsx        # tab navigator
    index.tsx          # Home
  user/[id].tsx        # dynamic route
components/
features/
  user/UserProfile.tsx
```

#### Navigation: validate route params

Deep links and dynamic routes deliver untrusted strings. Validate them with Zod before use.

```tsx
// app/user/[id].tsx
import { useLocalSearchParams, router } from 'expo-router'
import { z } from 'zod'
import { UserProfile } from '@/features/user/UserProfile'

const Params = z.object({ id: z.string().uuid() })

export default function UserRoute() {
  const parsed = Params.safeParse(useLocalSearchParams())
  if (!parsed.success) {
    router.replace('/not-found')
    return null
  }
  return <UserProfile userId={parsed.data.id} />
}
```

#### State: keep concerns separate

Do not duplicate server data into a client store. Each concern has its own home.

| Concern | Common choices |
|---------|------|
| Server state (remote data) | a server-cache library (TanStack Query, SWR) |
| Client/UI state | a lightweight store (Zustand, Jotai) or Context |
| Route/navigation state | Expo Router params |
| Form state | a form library (e.g. React Hook Form) + schema validation |
| Secrets / tokens | `expo-secure-store` |
| Non-secret persistence | `AsyncStorage` / MMKV |

Prefer local `useState` until state genuinely needs sharing.

#### Data fetching: a cache library + Zod

Use a server-cache library (TanStack Query, SWR) instead of fetch-in-`useEffect`. Validate at the boundary and infer types from the schema. Handle loading, error, and empty states explicitly. (Example uses TanStack Query.)

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { z } from 'zod'

const User = z.object({ id: z.string(), email: z.string().email() })
type User = z.infer<typeof User>

export function useUser(id: string) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: async (): Promise<User> => User.parse(await api.getUser(id)),
  })
}

export function useUpdateEmail(id: string) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (email: string) => api.updateEmail(id, email),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['user', id] }),
  })
}
```

#### Lists: virtualize, never map a big array in a ScrollView

```tsx
import { FlatList } from 'react-native'

<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}          // memoized
  initialNumToRender={10}
  windowSize={5}
/>
```

Use `FlashList` (Shopify) for large or heterogeneous lists.

#### Styling: pick one system

`StyleSheet.create()` is the framework-native option; utility-class libraries (e.g. NativeWind) are a common alternative. Choose one and stay consistent. Never build style objects inline in JSX on hot paths.

```tsx
// NativeWind
<View className="p-4 rounded-2xl bg-white">
  <Text className="text-base font-semibold">Hello</Text>
</View>

// StyleSheet
const styles = StyleSheet.create({ card: { padding: 16, borderRadius: 16, backgroundColor: '#fff' } })
<View style={styles.card}>...</View>
```

#### Native APIs: wrap in hooks, clean up effects

Keep Expo SDK calls and subscriptions inside `use*` hooks, not in JSX. Always clean up.

```tsx
import { useEffect, useState } from 'react'
import * as Location from 'expo-location'

type LocationState =
  | { status: 'loading' }
  | { status: 'denied' }
  | { status: 'granted'; coords: Location.LocationObjectCoords }

export function useCurrentLocation() {
  // Track status, not just coords — so the UI can tell "still loading" apart
  // from "permission denied" and show an actionable message.
  const [state, setState] = useState<LocationState>({ status: 'loading' })

  useEffect(() => {
    let active = true
    ;(async () => {
      const { status } = await Location.requestForegroundPermissionsAsync()
      if (status !== 'granted') {
        if (active) setState({ status: 'denied' })
        return
      }
      const pos = await Location.getCurrentPositionAsync({})
      if (active) setState({ status: 'granted', coords: pos.coords })
    })()
    return () => { active = false }   // ignore stale result after unmount
  }, [])

  return state
}
```

#### Secure storage for tokens

```tsx
import * as SecureStore from 'expo-secure-store'

await SecureStore.setItemAsync('auth_token', token)   // Keychain / Keystore
const token = await SecureStore.getItemAsync('auth_token')
```

### Code Examples

#### A full screen: route → query → list → states

```tsx
// app/(tabs)/orders.tsx
import { memo, useCallback } from 'react'
import { FlatList, Text, View } from 'react-native'
import { useQuery } from '@tanstack/react-query'
import { z } from 'zod'

const OrderSchema = z.object({ id: z.string(), total: z.number(), status: z.string() })
const OrdersSchema = z.array(OrderSchema)
type Order = z.infer<typeof OrderSchema>

function useOrders() {
  return useQuery({
    queryKey: ['orders'],
    queryFn: async () => OrdersSchema.parse(await api.listOrders()),
  })
}

// Memoized so its reference is stable across renders (see the lists guidance).
const OrderRow = memo(function OrderRow({ item }: { item: Order }) {
  return (
    <View className="px-4 py-3 border-b border-neutral-200">
      <Text className="font-medium">#{item.id}</Text>
      <Text className="text-neutral-500">{item.status} · ${item.total}</Text>
    </View>
  )
})

export default function OrdersScreen() {
  const { data, isLoading, isError, refetch, isRefetching } = useOrders()
  const renderItem = useCallback(({ item }: { item: Order }) => <OrderRow item={item} />, [])

  if (isLoading) return <Centered><Text>Loading…</Text></Centered>
  if (isError) return <Centered><Text accessibilityRole="alert">Could not load orders.</Text></Centered>
  if (!data?.length) return <Centered><Text>No orders yet.</Text></Centered>

  return (
    <FlatList
      data={data}
      keyExtractor={(o) => o.id}
      onRefresh={refetch}
      refreshing={isRefetching}
      renderItem={renderItem}
    />
  )
}
```

#### A form: React Hook Form + Zod resolver

```tsx
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { TextInput, Button, Text } from 'react-native'

const Schema = z.object({ email: z.string().email('Invalid email') })
type FormValues = z.infer<typeof Schema>

export function EmailForm({ onSubmit }: { onSubmit: (v: FormValues) => void }) {
  const { control, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(Schema),
    defaultValues: { email: '' },
  })

  return (
    <>
      <Controller
        control={control}
        name="email"
        render={({ field: { value, onChange, onBlur } }) => (
          <TextInput
            value={value}
            onChangeText={onChange}
            onBlur={onBlur}
            autoCapitalize="none"
            keyboardType="email-address"
            accessibilityLabel="Email address"
          />
        )}
      />
      {errors.email && <Text accessibilityRole="alert">{errors.email.message}</Text>}
      <Button title="Save" onPress={handleSubmit(onSubmit)} />
    </>
  )
}
```

### Anti-Patterns

```tsx
// WRONG: large array mapped inside a ScrollView (no virtualization, janky, high memory)
<ScrollView>{items.map((i) => <Row key={i.id} item={i} />)}</ScrollView>
// RIGHT: FlatList / FlashList

// WRONG: server data copied into a client store (two sources of truth, stale data)
const useStore = create((set) => ({ users: [], setUsers: (u) => set({ users: u }) }))
useEffect(() => { getUsers().then(setUsers) }, [])
// RIGHT: useQuery owns server state; derive what you need

// WRONG: tokens in AsyncStorage (not encrypted)
await AsyncStorage.setItem('auth_token', token)
// RIGHT: expo-secure-store

// WRONG: trusting deep-link params
const { id } = useLocalSearchParams(); fetchUser(id)
// RIGHT: validate with Zod before use

// WRONG: inline style object recreated every render on a hot path
<View style={{ padding: 16, backgroundColor: '#fff' }} />
// RIGHT: StyleSheet.create at module scope, or NativeWind className

// WRONG: real secret shipped in the bundle
const STRIPE_SECRET = 'sk_live_...'
// RIGHT: keep privileged calls server-side; ship only public keys protected by backend rules
```

### Best Practices

- Keep route files thin; put logic in screen components and `use*` hooks.
- Validate every external input (API responses, route params, push payloads) with Zod.
- Let TanStack Query own server state; keep client stores small.
- Always render loading, error, and empty states — never just a spinner with no fallback.
- Virtualize lists; memoize `renderItem`; provide a stable `keyExtractor`.
- Use `react-native-reanimated` for animation (UI thread); avoid heavy work on the JS thread.
- Store tokens in `expo-secure-store`; never trust the client for authorization.
- Respect safe areas, Dynamic Type, and accessibility roles/labels from the start.
- Confirm New Architecture compatibility for every native dependency before release.

### Related Skills

- `languages:typescript` (`references/standards.md`) — React/Next.js (web) patterns; useful for shared React concepts, but DOM-specific.
- `coding-standards` — TypeScript/JavaScript idioms that apply to RN code.
- `testing:test-driven-development`, `testing:browser-testing` — testing process (use Jest + React Native Testing Library, Maestro/Detox for RN).
- `security:security-audit` — general security checklist that complements the RN bundle/secret guidance above.

## React Native / Expo Performance

<!-- source: affaan-m/ECC rules/react-native/performance.md -->

> This file extends common/performance.md with React Native / Expo specific content.

### Rendering

- Memoize expensive components with `React.memo`; memoize callbacks/values passed to children with `useCallback`/`useMemo` only where they prevent real re-renders.
- Keep component state local and narrow — lifting state too high re-renders large subtrees.
- Avoid creating new objects/arrays/functions inline in props on hot paths; they break memoization.
- Split large screens so a state change re-renders the smallest possible subtree.

### Lists

- Use `FlatList`/`SectionList`, or `FlashList` (Shopify) for large or heterogeneous lists.
- Provide `keyExtractor`, a memoized `renderItem`, and stable item heights when possible (`getItemLayout`).
- Tune `initialNumToRender`, `windowSize`, `maxToRenderPerBatch` for heavy rows.
- Never render large data sets with `.map()` inside a `ScrollView`.

### Images & Assets

- Use `expo-image` for caching, priority, and placeholders; serve appropriately sized images.
- Avoid loading full-resolution images into small thumbnails.

### Animations

- Prefer `react-native-reanimated` (runs on the UI thread) over the JS-driven `Animated` API.
- For legacy `Animated`, set `useNativeDriver: true` where supported.
- Keep heavy computation off the JS thread; offload to Reanimated worklets or native modules.

### Runtime & Build

- Build on the **New Architecture** (Fabric + TurboModules). It is the default in recent Expo SDKs (opt-out still available on SDK 53–54) and is mandatory — cannot be disabled — from SDK 55+. Verify every native dependency is New-Arch compatible before shipping.
- Ensure **Hermes** is enabled (default in modern Expo) for faster startup and lower memory.
- Defer non-critical work after first paint; lazy-load heavy screens/modules.
- Use `InteractionManager.runAfterInteractions` for work that can wait until animations finish.

### Measuring

- Profile with the React DevTools profiler, the Hermes sampling profiler, and the in-app performance monitor. (Avoid Flipper — it is deprecated and not supported on the New Architecture.)
- Watch for: long lists without virtualization, oversized images, frequent full-tree re-renders, and synchronous work on the JS thread.

## React Native / Expo Testing

<!-- source: affaan-m/ECC rules/react-native/testing.md -->

> This file extends common/testing.md with React Native / Expo specific content.
> Coverage target and TDD workflow are inherited from common/testing.md (80% minimum, RED-GREEN-REFACTOR).

### Tooling

| Layer | Tool |
|-------|------|
| Unit / component | Jest + `@testing-library/react-native` (via `jest-expo` preset) |
| Hooks | `@testing-library/react-native` `renderHook` |
| E2E | Maestro (recommended, simple YAML flows) or Detox |
| Type safety | `tsc --noEmit` in CI |

### Component Tests

- Query by accessible role/label/text, not by `testID` unless necessary — this also enforces accessibility.
- Assert on user-visible behavior, not implementation details.
- Follow Arrange-Act-Assert.

```tsx
import { render, screen, fireEvent } from '@testing-library/react-native'

test('calls onSelect with the user id when pressed', () => {
  const onSelect = jest.fn()
  render(<UserCard user={{ id: '1', email: 'a@b.com' }} onSelect={onSelect} />)

  fireEvent.press(screen.getByText('a@b.com'))

  expect(onSelect).toHaveBeenCalledWith('1')
})
```

### Mocking

- Mock Expo SDK modules (camera, location, notifications, secure-store) at the test boundary.
- Wrap components that use TanStack Query in a `QueryClientProvider` with a fresh client per test.
- Mock navigation (`expo-router`) so screens render in isolation.

### E2E

- Cover critical flows only: auth, primary navigation, core transactions.
- Run E2E on CI against a built app (EAS Build) before release.

### What to test first

Use the `testing:test-driven-development` agent proactively for new features: write a failing test that captures the behavior, then implement.

## React Native / Expo Security

<!-- source: affaan-m/ECC rules/react-native/security.md -->

> This file extends common/security.md with React Native / Expo specific content.
> The mandatory pre-commit checklist and Security Response Protocol from common/security.md still apply.

### The Bundle Is Public

Treat everything shipped in the app as readable by an attacker. A mobile binary can be unpacked.

- NEVER ship real secrets (private API keys, service-role keys, signing secrets) in the JS bundle or `app.config`.
- Public/anon keys (e.g. Supabase anon key, Firebase config) are acceptable ONLY when protected by server-side rules (RLS, security rules). Enforce authorization on the backend, never in the client.
- Keep privileged operations behind your own server / edge functions.

### Secret & Token Storage

- Store auth tokens and sensitive values in `expo-secure-store` (Keychain / Keystore) — never in `AsyncStorage` or plain MMKV.
- Do not persist secrets in Redux/Zustand state that may be serialized to disk.

### Configuration

- Read environment via `expo-constants` / `app.config.ts` `extra`, and `EXPO_PUBLIC_*` only for genuinely public values.
- Keep build secrets in EAS secrets, not in the repo.

### Network & Data

- HTTPS only; reject cleartext. Consider certificate pinning for high-risk apps.
- Validate ALL external data (API responses, deep-link params, push payloads) with Zod before use.
- Validate and sanitize deep links and universal links — never route or grant access based on unvalidated params.

### Permissions & Privacy

- Request the minimum device permissions, at the moment they are needed, with clear rationale.
- Declare data collection accurately for App Store / Play Store privacy disclosures.

### Dependencies

- Run `expo-doctor` and `npm audit` regularly; keep the Expo SDK and native deps current.
- Use `/security-scan` (AgentShield) on the agent configuration itself.

## React Native / Expo Production Readiness

<!-- source: affaan-m/ECC rules/react-native/production-readiness.md -->

> Extends these standards to ship-grade concerns that style/pattern rules cannot encode by themselves.
> A clean codebase is necessary but not sufficient for production — these items are mandatory before release.

### Architecture

- Ship on the **New Architecture** (Fabric + TurboModules). It is the default in recent Expo SDKs and is mandatory (cannot be disabled) from SDK 55+. Audit native deps for compatibility.
- Pin the Expo SDK version; upgrade deliberately with `npx expo install --check` and test on both platforms.

### Build & Release (EAS)

- Use **EAS Build** for production binaries and **EAS Submit** for store delivery. Do not rely on local ad-hoc builds for release.
- Keep separate build profiles (`development`, `preview`, `production`) in `eas.json`.
- Manage signing credentials via EAS; never commit keystores or provisioning profiles.

### Over-the-Air Updates

- Use **EAS Update** (`expo-updates`) for JS-only fixes, with a defined runtime version policy.
- Never push native changes via OTA — those require a new store build.
- Roll out gradually and keep the ability to roll back.

### Observability

- Integrate crash + error reporting (e.g. **Sentry** via `@sentry/react-native`) in production builds.
- Add structured logging and, where useful, analytics — but strip verbose logs from release.
- Capture and surface failed network/mutation states; do not fail silently.

### Configuration & Versioning

- Bump `version` and `ios.buildNumber` / `android.versionCode` per release.
- Public config via `EXPO_PUBLIC_*`; real secrets via EAS secrets only.
- Validate required config at startup and fail fast with a clear message.

### Pre-Release Gate

Before shipping, all must pass:

- [ ] `tsc --noEmit` clean
- [ ] `npx expo lint` clean
- [ ] Tests green, coverage >= 80% (see testing.md)
- [ ] `npx expo-doctor` healthy
- [ ] Critical-flow E2E (Maestro/Detox) pass on a real build
- [ ] No secrets in bundle (see security.md)
- [ ] Crash reporting active and verified
- [ ] Tested on physical iOS and Android devices, not just simulators
