# TypeScript and JavaScript — angular

Part of `languages:typescript`. Load only when the project uses angular.

## Angular Coding Style

<!-- source: affaan-m/ECC rules/angular/coding-style.md -->

> This file extends common/coding-style.md with Angular specific content.

### Version Awareness

Always check the project's Angular version before writing code — features differ significantly between versions. Run `ng version` or inspect `package.json`. When creating a new project, do not pin a version unless the user specifies one.

After generating or modifying Angular code, always run `ng build` to catch errors before finishing.

### File Naming

Follow Angular CLI conventions — one artifact per file:

- `user-profile.component.ts` + `user-profile.component.html` + `user-profile.component.spec.ts`
- `user.service.ts`, `auth.guard.ts`, `date-format.pipe.ts`
- Feature folders: `features/users/`, `features/auth/`
- Generate with the CLI: `ng generate component features/users/user-card`

### Components

Prefer standalone components (v17+ default). Use `OnPush` change detection on all new components.

```typescript
@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './user-card.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserCardComponent {
  user = input.required<User>();
  select = output<string>();
}
```

### Dependency Injection

Use `inject()` over constructor injection. Keep constructors empty or remove them entirely.

```typescript
// CORRECT
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);
  private router = inject(Router);
}

// WRONG: Constructor injection is verbose and harder to tree-shake
constructor(private http: HttpClient, private router: Router) {}
```

Use `InjectionToken` for non-class dependencies:

```typescript
const API_URL = new InjectionToken<string>('API_URL');

// Provide:
{ provide: API_URL, useValue: 'https://api.example.com' }

// Consume:
private apiUrl = inject(API_URL);
```

### Signals

#### Core Primitives

```typescript
count = signal(0);
doubled = computed(() => this.count() * 2);

increment() {
  this.count.update(n => n + 1);
}
```

#### `linkedSignal` — Writable Derived State

Use `linkedSignal` when a signal must reset or adapt when a source changes, but also be independently writable:

```typescript
selectedOption = linkedSignal(() => this.options()[0]);
// Resets to first option when options changes, but user can override
```

#### `resource` — Async Data into Signals

Use `resource()` to fetch async data reactively without manual subscriptions:

```typescript
userResource = resource({
  request: () => ({ id: this.userId() }),
  loader: ({ request }) => fetch(`/api/users/${request.id}`).then(r => r.json()),
});

// Access: userResource.value(), userResource.isLoading(), userResource.error()
```

#### `effect` Usage

Use `effect()` only for side effects that must react to signal changes (logging, third-party DOM manipulation). Never use effects to synchronize signals — use `computed` or `linkedSignal` instead. For DOM work after render, use `afterRenderEffect`.

```typescript
// CORRECT: Side effect
effect(() => console.log('User changed:', this.user()));

// WRONG: Use computed instead
effect(() => { this.fullName.set(`${this.first()} ${this.last()}`); });
```

### Templates

Use v17+ block syntax. Always provide `track` in `@for`:

```html
@for (item of items(); track item.id) {
  <app-item [item]="item" />
}

@if (isLoading()) {
  <app-spinner />
} @else if (error()) {
  <app-error [message]="error()" />
} @else {
  <app-content [data]="data()" />
}
```

No logic in templates beyond simple conditionals — move to component methods or pipes.

### Forms

Choose the form strategy that matches the project's existing approach:

- **Signal Forms** (v21+): Preferred for new projects on v21+. Signal-based form state.
- **Reactive Forms**: `FormBuilder` + `FormGroup` + `FormControl`. Best for complex forms with dynamic validation.
- **Template-Driven Forms**: `ngModel`. Suitable for simple forms only.

```typescript
// Reactive Forms — standard approach for most apps
export class LoginComponent {
  private fb = inject(FormBuilder);

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  submit() {
    if (this.form.valid) {
      // use this.form.value
    }
  }
}
```

### Component Styles

Use component-level styles with `ViewEncapsulation.Emulated` (default). Avoid `ViewEncapsulation.None` unless building a design system that intentionally bleeds styles.

- Scope styles to the component — do not use global class names inside component stylesheets
- Use `:host` for host element styling
- Prefer CSS custom properties for themeable values

### Change Detection

- Default to `ChangeDetectionStrategy.OnPush` on all new components
- Signals and `async` pipe handle detection automatically — avoid `markForCheck()` and `detectChanges()`
- Never mutate `@Input()` objects in place when using OnPush

## Angular Patterns

<!-- source: affaan-m/ECC rules/angular/patterns.md -->

> This file extends common/patterns.md with Angular specific content.

### Smart / Dumb Component Split

Smart (container) components own data fetching and state. Dumb (presentational) components receive inputs and emit outputs only — no service injection.

```typescript
// Smart — owns data
@Component({ standalone: true, changeDetection: ChangeDetectionStrategy.OnPush })
export class UserPageComponent {
  private userService = inject(UserService);
  user = toSignal(this.userService.getUser(this.userId));
}
```

```html
<!-- Dumb — pure presentation -->
<app-user-card [user]="user()" (select)="onSelect($event)" />
```

### Service Layer

Services own all data access and business logic. Components delegate — no `HttpClient` in components.

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}
```

### Async Data with `resource`

Use `resource()` for reactive async fetching. Prefer over manual RxJS pipelines for simple data loading:

```typescript
export class UserDetailComponent {
  userId = input.required<string>();

  userResource = resource({
    request: () => ({ id: this.userId() }),
    loader: ({ request }) =>
      firstValueFrom(inject(UserService).getUser(request.id)),
  });
}
```

Access state: `userResource.value()`, `userResource.isLoading()`, `userResource.error()`, `userResource.reload()`.

### Signal State Patterns

```typescript
// Local mutable state
count = signal(0);

// Derived (never duplicated)
doubled = computed(() => this.count() * 2);

// Writable derived state that resets with source
selectedItem = linkedSignal(() => this.items()[0]);

// Bridge Observable to signal
users = toSignal(this.userService.getUsers(), { initialValue: [] });
```

Never store derived values in separate signals — use `computed`. Never use `effect` to sync signals — use `computed` or `linkedSignal`.

### Subscription Cleanup

Use `takeUntilDestroyed()` for all manual subscriptions. Never use manual `ngOnDestroy` + `Subject` + `takeUntil` on new code.

```typescript
export class UserComponent {
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    this.userService.updates$
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(update => this.handleUpdate(update));
  }
}
```

### Routing

#### Route Definition

```typescript
// app.routes.ts
export const routes: Routes = [
  { path: '', component: HomeComponent },
  {
    path: 'admin',
    canMatch: [authGuard],           // CanMatch prevents loading the chunk at all
    loadChildren: () => import('./admin/admin.routes').then(m => m.ADMIN_ROUTES),
  },
  {
    path: 'users/:id',
    resolve: { user: userResolver },
    component: UserDetailComponent,
  },
];
```

- Use `canMatch` over `canActivate` when the route module should not load for unauthorized users
- Lazy-load all feature modules with `loadChildren`
- Pre-fetch data with `resolve` to avoid loading states in components

#### Functional Guards

```typescript
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  return auth.isAuthenticated()
    ? true
    : inject(Router).createUrlTree(['/login']);
};
```

#### Data Resolvers

```typescript
export const userResolver: ResolveFn<User> = (route) => {
  return inject(UserService).getUser(route.paramMap.get('id')!);
};
```

#### View Transitions

Enable smooth route transitions with the View Transitions API:

```typescript
// app.config.ts
provideRouter(routes, withViewTransitions())
```

### Dependency Injection Patterns

#### Scoped Providers

Provide services at component or route level when they should not be singletons:

```typescript
@Component({
  providers: [UserEditService],   // scoped to this component subtree
})
export class UserEditComponent {}
```

#### `InjectionToken`

```typescript
export const CONFIG = new InjectionToken<AppConfig>('APP_CONFIG');

// In providers:
{ provide: CONFIG, useValue: appConfig }
{ provide: CONFIG, useFactory: () => loadConfig(), deps: [] }

// Consume:
private config = inject(CONFIG);
```

#### `viewProviders` vs `providers`

- `providers`: Available to the component and all its content children
- `viewProviders`: Available only to the component's own view (not projected content)

### HTTP Interceptors

Use functional interceptors (v15+) for auth, error handling, and retries:

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).token();
  if (!token) return next(req);
  return next(req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }));
};
```

Register in `app.config.ts`:

```typescript
provideHttpClient(withInterceptors([authInterceptor, errorInterceptor]))
```

### RxJS Operators

- `switchMap` — search, navigation (cancels previous)
- `mergeMap` — independent parallel requests
- `exhaustMap` — form submissions (ignores until complete)
- Always handle errors with `catchError` — never let streams die silently

```typescript
search$ = this.query$.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  switchMap(q => this.service.search(q).pipe(catchError(() => of([])))),
);
```

### Forms

Match the project's existing form strategy. For new v21+ apps, prefer signal forms.

```typescript
// Reactive Forms — standard for complex forms
export class UserFormComponent {
  private fb = inject(FormBuilder);

  form = this.fb.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
  });
}
```

### Rendering Strategies

- **CSR** (default): Standard SPA
- **SSR + Hydration**: `ng add @angular/ssr` — improves FCP and SEO
- **SSG (Prerendering)**: Static pages at build time for content-heavy routes

When using SSR, avoid `window`, `document`, `localStorage` directly — use `isPlatformBrowser` or `DOCUMENT` token.

### Accessibility

Use Angular CDK for headless, accessible components (Accordion, Listbox, Combobox, Menu, Tabs, Toolbar, Tree, Grid). Style ARIA attributes rather than managing them manually:

```css
[aria-selected="true"] { background: var(--color-selected); }
```

### Skill Reference

See skill: `languages:typescript` (`references/frameworks/angular.md`) for deep guidance on signals, forms, routing, DI, SSR, and accessibility patterns.

## Angular Developer Guidelines

<!-- source: affaan-m/ECC pi/core/skills/angular-developer/SKILL.md -->

### When to Activate

- Working in any Angular project or codebase
- Creating or scaffolding a new Angular project, application, or library
- Generating components, services, directives, pipes, guards, or resolvers
- Implementing reactivity with Angular Signals, `linkedSignal`, or `resource`
- Working with Angular forms (signal forms, reactive forms, or template-driven)
- Setting up dependency injection, routing, lazy loading, or route guards
- Adding accessibility (ARIA), animations, or component styling
- Writing or debugging Angular-specific tests (unit, component harness, E2E)
- Configuring Angular CLI tooling or the Angular MCP server

1. Always analyze the project's Angular version before providing guidance, as best practices and available features can vary significantly between versions. If creating a new project with Angular CLI, do not specify a version unless prompted by the user.

2. When generating code, follow Angular's style guide and best practices for maintainability and performance. Use the Angular CLI for scaffolding components, services, directives, pipes, and routes to ensure consistency.

3. Once you finish generating code, run `ng build` to ensure there are no build errors. If there are errors, analyze the error messages and fix them before proceeding. Do not skip this step, as it is critical for ensuring the generated code is correct and functional.

### Creating New Projects

If no guidelines are provided by the user, use these defaults when creating a new Angular project:

1. Use the latest stable version of Angular unless the user specifies otherwise.
2. Prefer Signal Forms for new projects only when the target Angular version supports them. Find out more.

**Execution Rules for `ng new`:**
When asked to create a new Angular project, you must determine the correct execution command by following these strict steps:

**Step 1: Check for an explicit user version.**

- **IF** the user requests a specific version (e.g., Angular 15), bypass local installations and strictly use `npx`.
- **Command:** `npx @angular/cli@<requested_version> new <project-name>`

**Step 2: Check for an existing Angular installation.**

- **IF** no specific version is requested, run `ng version` in the terminal to check if the Angular CLI is already installed on the system.
- **IF** the command succeeds and returns an installed version, use the local/global installation directly.
- **Command:** `ng new <project-name>`

**Step 3: Fallback to Latest.**

- **IF** no specific version is requested AND the `ng version` command fails (indicating no Angular installation exists), you must use `npx` to fetch the latest version.
- **Command:** `npx @angular/cli@latest new <project-name>`

### Components

When working with Angular components, consult the following references based on the task:

- **Fundamentals**: Anatomy, metadata, core concepts, and template control flow (@if, @for, @switch). Read components.md
- **Inputs**: Signal-based inputs, transforms, and model inputs. Read inputs.md
- **Outputs**: Signal-based outputs and custom event best practices. Read outputs.md
- **Host Elements**: Host bindings and attribute injection. Read host-elements.md

If you require deeper documentation not found in the references above, read the documentation at `https://angular.dev/guide/components`.

### Reactivity and Data Management

When managing state and data reactivity, use Angular Signals and consult the following references:

- **Signals Overview**: Core signal concepts (`signal`, `computed`), reactive contexts, and `untracked`. Read signals-overview.md
- **Dependent State (`linkedSignal`)**: Creating writable state linked to source signals. Read linked-signal.md
- **Async Reactivity (`resource`)**: Fetching asynchronous data directly into signal state. Read resource.md
- **Side Effects (`effect`)**: Logging, third-party DOM manipulation (`afterRenderEffect`), and when NOT to use effects. Read effects.md

### Forms

In most cases for new apps, **prefer signal forms**. When making a forms decision, analyze the project and consider the following guidelines:

- If the application version supports Signal Forms and this is a new form, **prefer signal forms**.
- For older applications or existing forms, match the application's current form strategy.

- **Signal Forms**: Use signals for form state management. Read signal-forms.md
- **Template-driven forms**: Use for simple forms. Read template-driven-forms.md
- **Reactive forms**: Use for complex forms. Read reactive-forms.md

### Dependency Injection

When implementing dependency injection in Angular, follow these guidelines:

- **Fundamentals**: Overview of Dependency Injection, services, and the `inject()` function. Read di-fundamentals.md
- **Creating and Using Services**: Creating services, the `providedIn: 'root'` option, and injecting into components or other services. Read creating-services.md
- **Defining Dependency Providers**: Automatic vs manual provision, `InjectionToken`, `useClass`, `useValue`, `useFactory`, and scopes. Read defining-providers.md
- **Injection Context**: Where `inject()` is allowed, `runInInjectionContext`, and `assertInInjectionContext`. Read injection-context.md
- **Hierarchical Injectors**: The `EnvironmentInjector` vs `ElementInjector`, resolution rules, modifiers (`optional`, `skipSelf`), and `providers` vs `viewProviders`. Read hierarchical-injectors.md

### Angular Aria

When building accessible custom components for any of the following patterns: Accordion, Listbox, Combobox, Menu, Tabs, Toolbar, Tree, Grid, consult the following reference:

- **Angular Aria Components**: Building headless, accessible components (Accordion, Listbox, Combobox, Menu, Tabs, Toolbar, Tree, Grid) and styling ARIA attributes. Read angular-aria.md

### Routing

When implementing navigation in Angular, consult the following references:

- **Define Routes**: URL paths, static vs dynamic segments, wildcards, and redirects. Read define-routes.md
- **Route Loading Strategies**: Eager vs lazy loading, and context-aware loading. Read loading-strategies.md
- **Show Routes with Outlets**: Using `<router-outlet>`, nested outlets, and named outlets. Read show-routes-with-outlets.md
- **Navigate to Routes**: Declarative navigation with `RouterLink` and programmatic navigation with `Router`. Read navigate-to-routes.md
- **Control Route Access with Guards**: Implementing `CanActivate`, `CanMatch`, and other guards for security. Read route-guards.md
- **Data Resolvers**: Pre-fetching data before route activation with `ResolveFn`. Read data-resolvers.md
- **Router Lifecycle and Events**: Chronological order of navigation events and debugging. Read router-lifecycle.md
- **Rendering Strategies**: CSR, SSG (Prerendering), and SSR with hydration. Read rendering-strategies.md
- **Route Transition Animations**: Enabling and customizing the View Transitions API. Read route-animations.md

If you require deeper documentation or more context, visit the [official Angular Routing guide](https://angular.dev/guide/routing).

### Styling and Animations

When implementing styling and animations in Angular, consult the following references:

- **Using Tailwind CSS with Angular**: Integrating Tailwind CSS into Angular projects. Read tailwind-css.md
- **Angular Animations**: Using native CSS (recommended) or the legacy DSL for dynamic effects. Read angular-animations.md
- **Styling components**: Best practices for component styles and encapsulation. Read component-styling.md

### Testing

When writing or updating tests, consult the following references based on the task:

- **Fundamentals**: Best practices for unit testing, async patterns, and `TestBed`. Read testing-fundamentals.md
- **Component Harnesses**: Standard patterns for robust component interaction. Read component-harnesses.md
- **Router Testing**: Using `RouterTestingHarness` for reliable navigation tests. Read router-testing.md
- **End-to-End (E2E) Testing**: Best practices for E2E tests with Cypress or Playwright. Read e2e-testing.md

### Tooling

When working with Angular tooling, consult the following references:

- **Angular CLI**: Creating applications, generating code (components, routes, services), serving, and building. Read cli.md
- **Angular MCP Server**: Available tools, configuration, and experimental features. Read mcp.md

### Anti-Patterns

- Using `null` or `undefined` as initial signal form field values — use `''`, `0`, or `[]` instead
- Accessing form field state flags without calling the field first: `form.field.valid()` — use `form.field().valid()`
- Starting new forms with older form APIs when the target Angular version supports Signal Forms
- Setting `min`, `max`, `value`, `disabled`, or `readonly` HTML attributes on `[formField]` inputs — define these as schema rules instead
- Calling `inject()` outside an injection context — use `runInInjectionContext` when needed
- Using `effect()` for derived state that should use `computed()`
- Referencing `$parent.$index` in nested `@for` loops — Angular does not support `$parent`; use `let outerIdx = $index` instead

### Related Skills

- `testing:test-driven-development` — test-driven development workflow applicable to Angular components and services
- `security:security-audit` — security checklist for web applications including Angular-specific concerns
- `languages:typescript` (`references/standards.md`) — general frontend patterns for context on React/Next.js approaches

## Angular Testing

<!-- source: affaan-m/ECC rules/angular/testing.md -->

> This file extends common/testing.md with Angular specific content.

### Test Runner

Use the test runner configured by the project. Check `angular.json` and `package.json`; Angular projects commonly use Vitest, Jest, or Jasmine + Karma.

```bash
ng test               # watch mode
ng test --no-watch    # CI mode
```

### TestBed Setup

For standalone components, import the component directly. Call `compileComponents()` for components with external templates.

```typescript
describe('UserCardComponent', () => {
  let fixture: ComponentFixture<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
  });
});
```

### Signal Inputs

Set signal-based inputs via `fixture.componentRef.setInput()`:

```typescript
fixture.componentRef.setInput('user', mockUser);
fixture.detectChanges();
```

### Component Harnesses

Prefer Angular CDK component harnesses over direct DOM queries for UI interaction. Harnesses are more resilient to markup changes.

```typescript
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatButtonHarness } from '@angular/material/button/testing';

let loader: HarnessLoader;

beforeEach(() => {
  loader = TestbedHarnessEnvironment.loader(fixture);
});

it('triggers save on button click', async () => {
  const button = await loader.getHarness(MatButtonHarness.with({ text: 'Save' }));
  await button.click();
  expect(saveSpy).toHaveBeenCalled();
});
```

### Router Testing

Use `RouterTestingHarness` for components that depend on the router:

```typescript
import { RouterTestingHarness } from '@angular/router/testing';

it('renders user on navigation', async () => {
  const harness = await RouterTestingHarness.create();
  const component = await harness.navigateByUrl('/users/1', UserDetailComponent);
  expect(component.userId()).toBe('1');
});
```

### Async Testing

Use `fakeAsync` + `tick` for controlled async. Use `waitForAsync` for real async with `fixture.whenStable()`.

```typescript
it('loads user after delay', fakeAsync(() => {
  const service = TestBed.inject(UserService);
  vi.spyOn(service, 'getUser').mockReturnValue(of(mockUser));

  fixture.detectChanges();
  tick();
  fixture.detectChanges();

  expect(fixture.nativeElement.querySelector('.name').textContent).toBe(mockUser.name);
}));
```

### HTTP Testing

```typescript
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { HttpTestingController } from '@angular/common/http/testing';

beforeEach(() => {
  TestBed.configureTestingModule({
    providers: [provideHttpClient(), provideHttpClientTesting()],
  });
  httpMock = TestBed.inject(HttpTestingController);
});

afterEach(() => httpMock.verify());
```

### Service Testing

Inject services directly without a component fixture:

```typescript
describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(UserService);
  });
});
```

### What to Test

- **Services**: All public methods, error paths, HTTP interactions
- **Components**: Input/output bindings, rendered output for key states, user interactions via harnesses
- **Pipes**: Pure transformation — plain unit tests, no TestBed needed
- **Guards/Resolvers**: Return values for allowed and denied states using `RouterTestingHarness`

### E2E Testing

Use the project's configured E2E framework, such as Cypress or Playwright, for critical user flows.

```typescript
describe('Login flow', () => {
  it('redirects to dashboard on valid credentials', () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type('user@example.com');
    cy.get('[data-cy=password]').type('password123');
    cy.get('[data-cy=submit]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

- Add `data-cy` attributes to interactive elements for stable selectors
- Do not rely on CSS classes or text content for selectors in E2E tests

### Coverage

Target ≥80% for services and pipes. Components: test behaviour, not implementation details.

### Skill Reference

See skill: `languages:typescript` (`references/frameworks/angular.md`) for comprehensive testing patterns, harness usage, and async best practices.

## Angular Security

<!-- source: affaan-m/ECC rules/angular/security.md -->

> This file extends common/security.md with Angular specific content.

### XSS Prevention

Angular auto-sanitizes bound values. Never bypass the sanitizer on user-controlled input.

```typescript
// WRONG: Bypasses sanitization — XSS risk
this.safeHtml = this.sanitizer.bypassSecurityTrustHtml(userInput);

// CORRECT: Sanitize explicitly before trusting
this.safeHtml = this.sanitizer.sanitize(SecurityContext.HTML, userInput);
```

- Never use `bypassSecurityTrust*` methods without a documented, reviewed reason
- Avoid `[innerHTML]` with untrusted content — use `innerText` or a sanitizing pipe
- Never bind `[href]` to user input — Angular does not block `javascript:` URLs in all contexts
- Never construct template strings from user data

### HTTP Security

Use `HttpClient` exclusively — never raw `fetch()` or `XHR` unless no alternative exists.

```typescript
// WRONG: Bypasses interceptors (auth headers, error handling, logging)
const res = await fetch('/api/users');

// CORRECT
users$ = this.http.get<User[]>('/api/users');
```

- Attach auth tokens via interceptors — never hardcode in individual service calls
- Type and validate API responses — treat external data as `unknown` at the boundary
- Never log HTTP responses that may contain tokens, PII, or credentials

### Secret Management

```typescript
// WRONG: Hardcoded secret in source
const apiKey = 'sk-live-xxxx';

// CORRECT: Injected via environment
import { environment } from '../environments/environment';
const apiKey = environment.apiKey;
```

- Treat `environment.ts` as a config shape — never store real secrets in source-controlled environment files
- Inject production secrets via CI/CD (environment variables, secret managers)

### Route Guards

Every authenticated or role-restricted route must have a guard. Never rely on hiding UI elements alone.

```typescript
{
  path: 'admin',
  canMatch: [authGuard, roleGuard('admin')],
  loadChildren: () => import('./admin/admin.routes'),
}
```

Use `canMatch` for sensitive routes — it prevents the route module from loading at all for unauthorized users.

### SSR Security

When using Angular SSR:

- Never expose server-side environment variables to the client via `TransferState` unless they are intentionally public
- Sanitize all inputs before server-side rendering — DOM-based XSS can occur server-side too
- Avoid `window`, `document`, `localStorage` on the server — gate with `isPlatformBrowser` or inject via `DOCUMENT` token

### Content Security Policy

Configure CSP headers server-side. Avoid `unsafe-inline` in `script-src`. When using SSR with inline scripts, use nonces via Angular's CSP support.

### Agent Support

- Use **security-reviewer** skill for comprehensive security audits
