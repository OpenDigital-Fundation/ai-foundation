# Dart and Flutter — Standards and idioms

Part of `languages:dart`. Load when writing or refactoring code: style, idioms, patterns, project layout.

## Dart/Flutter Coding Style

<!-- source: affaan-m/ECC rules/dart/coding-style.md -->

> This file extends common/coding-style.md with Dart and Flutter-specific content.

### Formatting

- **dart format** for all `.dart` files — enforced in CI (`dart format --set-exit-if-changed .`)
- Line length: 80 characters (dart format default)
- Trailing commas on multi-line argument/parameter lists to improve diffs and formatting

### Immutability

- Prefer `final` for local variables and `const` for compile-time constants
- Use `const` constructors wherever all fields are `final`
- Return unmodifiable collections from public APIs (`List.unmodifiable`, `Map.unmodifiable`)
- Use `copyWith()` for state mutations in immutable state classes

```dart
// BAD
var count = 0;
List<String> items = ['a', 'b'];

// GOOD
final count = 0;
const items = ['a', 'b'];
```

### Naming

Follow Dart conventions:
- `camelCase` for variables, parameters, and named constructors
- `PascalCase` for classes, enums, typedefs, and extensions
- `snake_case` for file names and library names
- `SCREAMING_SNAKE_CASE` for constants declared with `const` at top level
- Prefix private members with `_`
- Extension names describe the type they extend: `StringExtensions`, not `MyHelpers`

### Null Safety

- Avoid `!` (bang operator) — prefer `?.`, `??`, `if (x != null)`, or Dart 3 pattern matching; reserve `!` only where a null value is a programming error and crashing is the right behaviour
- Avoid `late` unless initialization is guaranteed before first use (prefer nullable or constructor init)
- Use `required` for constructor parameters that must always be provided

```dart
// BAD — crashes at runtime if user is null
final name = user!.name;

// GOOD — null-aware operators
final name = user?.name ?? 'Unknown';

// GOOD — Dart 3 pattern matching (exhaustive, compiler-checked)
final name = switch (user) {
  User(:final name) => name,
  null => 'Unknown',
};

// GOOD — early-return null guard
String getUserName(User? user) {
  if (user == null) return 'Unknown';
  return user.name; // promoted to non-null after the guard
}
```

### Sealed Types and Pattern Matching (Dart 3+)

Use sealed classes to model closed state hierarchies:

```dart
sealed class AsyncState<T> {
  const AsyncState();
}

final class Loading<T> extends AsyncState<T> {
  const Loading();
}

final class Success<T> extends AsyncState<T> {
  const Success(this.data);
  final T data;
}

final class Failure<T> extends AsyncState<T> {
  const Failure(this.error);
  final Object error;
}
```

Always use exhaustive `switch` with sealed types — no default/wildcard:

```dart
// BAD
if (state is Loading) { ... }

// GOOD
return switch (state) {
  Loading() => const CircularProgressIndicator(),
  Success(:final data) => DataWidget(data),
  Failure(:final error) => ErrorWidget(error.toString()),
};
```

### Error Handling

- Specify exception types in `on` clauses — never use bare `catch (e)`
- Never catch `Error` subtypes — they indicate programming bugs
- Use `Result`-style types or sealed classes for recoverable errors
- Avoid using exceptions for control flow

```dart
// BAD
try {
  await fetchUser();
} catch (e) {
  log(e.toString());
}

// GOOD
try {
  await fetchUser();
} on NetworkException catch (e) {
  log('Network error: ${e.message}');
} on NotFoundException {
  handleNotFound();
}
```

### Async / Futures

- Always `await` Futures or explicitly call `unawaited()` to signal intentional fire-and-forget
- Never mark a function `async` if it never `await`s anything
- Use `Future.wait` / `Future.any` for concurrent operations
- Check `context.mounted` before using `BuildContext` after any `await` (Flutter 3.7+)

```dart
// BAD — ignoring Future
fetchData(); // fire-and-forget without marking intent

// GOOD
unawaited(fetchData()); // explicit fire-and-forget
await fetchData();      // or properly awaited
```

### Imports

- Use `package:` imports throughout — never relative imports (`../`) for cross-feature or cross-layer code
- Order: `dart:` → external `package:` → internal `package:` (same package)
- No unused imports — `dart analyze` enforces this with `unused_import`

### Code Generation

- Generated files (`.g.dart`, `.freezed.dart`, `.gr.dart`) must be committed or gitignored consistently — pick one strategy per project
- Never manually edit generated files
- Keep generator annotations (`@JsonSerializable`, `@freezed`, `@riverpod`, etc.) on the canonical source file only

## Dart/Flutter Patterns

<!-- source: affaan-m/ECC rules/dart/patterns.md -->

> This file extends common/patterns.md with Dart, Flutter, and common ecosystem-specific content.

### Repository Pattern

```dart
abstract interface class UserRepository {
  Future<User?> getById(String id);
  Future<List<User>> getAll();
  Stream<List<User>> watchAll();
  Future<void> save(User user);
  Future<void> delete(String id);
}

class UserRepositoryImpl implements UserRepository {
  const UserRepositoryImpl(this._remote, this._local);

  final UserRemoteDataSource _remote;
  final UserLocalDataSource _local;

  @override
  Future<User?> getById(String id) async {
    final local = await _local.getById(id);
    if (local != null) return local;
    final remote = await _remote.getById(id);
    if (remote != null) await _local.save(remote);
    return remote;
  }

  @override
  Future<List<User>> getAll() async {
    final remote = await _remote.getAll();
    for (final user in remote) {
      await _local.save(user);
    }
    return remote;
  }

  @override
  Stream<List<User>> watchAll() => _local.watchAll();

  @override
  Future<void> save(User user) => _local.save(user);

  @override
  Future<void> delete(String id) async {
    await _remote.delete(id);
    await _local.delete(id);
  }
}
```

### State Management: BLoC/Cubit

```dart
// Cubit — simple state transitions
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
}

// BLoC — event-driven
@immutable
sealed class CartEvent {}
class CartItemAdded extends CartEvent { CartItemAdded(this.item); final Item item; }
class CartItemRemoved extends CartEvent { CartItemRemoved(this.id); final String id; }
class CartCleared extends CartEvent {}

@immutable
class CartState {
  const CartState({this.items = const []});
  final List<Item> items;
  CartState copyWith({List<Item>? items}) => CartState(items: items ?? this.items);
}

class CartBloc extends Bloc<CartEvent, CartState> {
  CartBloc() : super(const CartState()) {
    on<CartItemAdded>((event, emit) =>
        emit(state.copyWith(items: [...state.items, event.item])));
    on<CartItemRemoved>((event, emit) =>
        emit(state.copyWith(items: state.items.where((i) => i.id != event.id).toList())));
    on<CartCleared>((_, emit) => emit(const CartState()));
  }
}
```

### State Management: Riverpod

```dart
// Simple provider
@riverpod
Future<List<User>> users(Ref ref) async {
  final repo = ref.watch(userRepositoryProvider);
  return repo.getAll();
}

// Notifier for mutable state
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  List<Item> build() => [];

  void add(Item item) => state = [...state, item];
  void remove(String id) => state = state.where((i) => i.id != id).toList();
  void clear() => state = [];
}

// ConsumerWidget
class CartPage extends ConsumerWidget {
  const CartPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final items = ref.watch(cartNotifierProvider);
    return ListView(
      children: items.map((item) => CartItemTile(item: item)).toList(),
    );
  }
}
```

### Dependency Injection

Constructor injection is preferred. Use `get_it` or Riverpod providers at composition root:

```dart
// get_it registration (in a setup file)
void setupDependencies() {
  final di = GetIt.instance;
  di.registerSingleton<ApiClient>(ApiClient(baseUrl: Env.apiUrl));
  di.registerSingleton<UserRepository>(
    UserRepositoryImpl(di<ApiClient>(), di<LocalDatabase>()),
  );
  di.registerFactory(() => UserListViewModel(di<UserRepository>()));
}
```

### ViewModel Pattern (without BLoC/Riverpod)

```dart
class UserListViewModel extends ChangeNotifier {
  UserListViewModel(this._repository);

  final UserRepository _repository;

  AsyncState<List<User>> _state = const Loading();
  AsyncState<List<User>> get state => _state;

  Future<void> load() async {
    _state = const Loading();
    notifyListeners();
    try {
      final users = await _repository.getAll();
      _state = Success(users);
    } on Exception catch (e) {
      _state = Failure(e);
    }
    notifyListeners();
  }
}
```

### UseCase Pattern

```dart
class GetUserUseCase {
  const GetUserUseCase(this._repository);
  final UserRepository _repository;

  Future<User?> call(String id) => _repository.getById(id);
}

class CreateUserUseCase {
  const CreateUserUseCase(this._repository, this._idGenerator);
  final UserRepository _repository;
  final IdGenerator _idGenerator; // injected — domain layer must not depend on uuid package directly

  Future<void> call(CreateUserInput input) async {
    // Validate, apply business rules, then persist
    final user = User(id: _idGenerator.generate(), name: input.name, email: input.email);
    await _repository.save(user);
  }
}
```

### Immutable State with freezed

```dart
@freezed
class UserState with _$UserState {
  const factory UserState({
    @Default([]) List<User> users,
    @Default(false) bool isLoading,
    String? errorMessage,
  }) = _UserState;
}
```

### Clean Architecture Layer Boundaries

```
lib/
├── domain/              # Pure Dart — no Flutter, no external packages
│   ├── entities/
│   ├── repositories/    # Abstract interfaces
│   └── usecases/
├── data/                # Implements domain interfaces
│   ├── datasources/
│   ├── models/          # DTOs with fromJson/toJson
│   └── repositories/
└── presentation/        # Flutter widgets + state management
    ├── pages/
    ├── widgets/
    └── providers/ (or blocs/ or viewmodels/)
```

- Domain must not import `package:flutter` or any data-layer package
- Data layer maps DTOs to domain entities at repository boundaries
- Presentation calls use cases, not repositories directly

### Navigation (GoRouter)

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/users/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return UserDetailPage(userId: id);
      },
    ),
  ],
  // refreshListenable re-evaluates redirect whenever auth state changes
  refreshListenable: GoRouterRefreshStream(authCubit.stream),
  redirect: (context, state) {
    final isLoggedIn = context.read<AuthCubit>().state is AuthAuthenticated;
    if (!isLoggedIn && !state.matchedLocation.startsWith('/login')) {
      return '/login';
    }
    return null;
  },
);
```

### References

See skill: `languages:dart` (`references/review.md`) for the comprehensive review checklist.
See skill: `languages:jvm` (`references/frameworks/compose-multiplatform.md`) for Kotlin Multiplatform/Flutter interop patterns.

## Dart/Flutter Patterns

<!-- source: affaan-m/ECC pi/core/skills/dart-flutter-patterns/SKILL.md -->

### When to Use

Use this skill when:
- Starting a new Flutter feature and need idiomatic patterns for state management, navigation, or data access
- Reviewing or writing Dart code and need guidance on null safety, sealed types, or async composition
- Setting up a new Flutter project and choosing between BLoC, Riverpod, or Provider
- Implementing secure HTTP clients, WebView integration, or local storage
- Writing tests for Flutter widgets, Cubits, or Riverpod providers
- Wiring up GoRouter with authentication guards

### How It Works

This skill provides copy-paste-ready Dart/Flutter code patterns organized by concern:
1. **Null safety** — avoid `!`, prefer `?.`/`??`/pattern matching
2. **Immutable state** — sealed classes, `freezed`, `copyWith`
3. **Async composition** — concurrent `Future.wait`, safe `BuildContext` after `await`
4. **Widget architecture** — extract to classes (not methods), `const` propagation, scoped rebuilds
5. **State management** — BLoC/Cubit events, Riverpod notifiers and derived providers
6. **Navigation** — GoRouter with reactive auth guards via `refreshListenable`
7. **Networking** — Dio with interceptors, token refresh with one-time retry guard
8. **Error handling** — global capture, `ErrorWidget.builder`, crashlytics wiring
9. **Testing** — unit (BLoC test), widget (ProviderScope overrides), fakes over mocks

### Examples

```dart
// Sealed state — prevents impossible states
sealed class AsyncState<T> {}
final class Loading<T> extends AsyncState<T> {}
final class Success<T> extends AsyncState<T> { final T data; const Success(this.data); }
final class Failure<T> extends AsyncState<T> { final Object error; const Failure(this.error); }

// GoRouter with reactive auth redirect
final router = GoRouter(
  refreshListenable: GoRouterRefreshStream(authCubit.stream),
  redirect: (context, state) {
    final authed = context.read<AuthCubit>().state is AuthAuthenticated;
    if (!authed && !state.matchedLocation.startsWith('/login')) return '/login';
    return null;
  },
  routes: [...],
);

// Riverpod derived provider with safe firstWhereOrNull
@riverpod
double cartTotal(Ref ref) {
  final cart = ref.watch(cartNotifierProvider);
  final products = ref.watch(productsProvider).valueOrNull ?? [];
  return cart.fold(0.0, (total, item) {
    final product = products.firstWhereOrNull((p) => p.id == item.productId);
    return total + (product?.price ?? 0) * item.quantity;
  });
}
```

---

Practical, production-ready patterns for Dart and Flutter applications. Library-agnostic where possible, with explicit coverage of the most common ecosystem packages.

---

### 1. Null Safety Fundamentals

#### Prefer Patterns Over Bang Operator

```dart
// BAD — crashes at runtime if null
final name = user!.name;

// GOOD — provide fallback
final name = user?.name ?? 'Unknown';

// GOOD — Dart 3 pattern matching (preferred for complex cases)
final display = switch (user) {
  User(:final name, :final email) => '$name <$email>',
  null => 'Guest',
};

// GOOD — guard early return
String getUserName(User? user) {
  if (user == null) return 'Unknown';
  return user.name; // promoted to non-null after check
}
```

#### Avoid `late` Overuse

```dart
// BAD — defers null error to runtime
late String userId;

// GOOD — nullable with explicit initialization
String? userId;

// OK — use late only when initialization is guaranteed before first access
// (e.g., in initState() before any widget interaction)
late final AnimationController _controller;

@override
void initState() {
  super.initState();
  _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 300));
}
```

---

### 2. Immutable State

#### Sealed Classes for State Hierarchies

```dart
sealed class UserState {}

final class UserInitial extends UserState {}

final class UserLoading extends UserState {}

final class UserLoaded extends UserState {
  const UserLoaded(this.user);
  final User user;
}

final class UserError extends UserState {
  const UserError(this.message);
  final String message;
}

// Exhaustive switch — compiler enforces all branches
Widget buildFrom(UserState state) => switch (state) {
  UserInitial() => const SizedBox.shrink(),
  UserLoading() => const CircularProgressIndicator(),
  UserLoaded(:final user) => UserCard(user: user),
  UserError(:final message) => ErrorText(message),
};
```

#### Freezed for Boilerplate-Free Immutability

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @Default(false) bool isAdmin,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Usage
final user = User(id: '1', name: 'Alice', email: 'alice@example.com');
final updated = user.copyWith(name: 'Alice Smith'); // immutable update
final json = user.toJson();
final fromJson = User.fromJson(json);
```

---

### 3. Async Composition

#### Structured Concurrency with Future.wait

```dart
Future<DashboardData> loadDashboard(UserRepository users, OrderRepository orders) async {
  // Run concurrently — don't await sequentially
  final (userList, orderList) = await (
    users.getAll(),
    orders.getRecent(),
  ).wait; // Dart 3 record destructuring + Future.wait extension

  return DashboardData(users: userList, orders: orderList);
}
```

#### Stream Patterns

```dart
// Repository exposes reactive streams for live data
Stream<List<Item>> watchCartItems() => _db
    .watchTable('cart_items')
    .map((rows) => rows.map(Item.fromRow).toList());

// In widget layer — declarative, no manual subscription
StreamBuilder<List<Item>>(
  stream: cartRepository.watchCartItems(),
  builder: (context, snapshot) => switch (snapshot) {
    AsyncSnapshot(connectionState: ConnectionState.waiting) =>
        const CircularProgressIndicator(),
    AsyncSnapshot(:final error?) => ErrorWidget(error.toString()),
    AsyncSnapshot(:final data?) => CartList(items: data),
    _ => const SizedBox.shrink(),
  },
)
```

#### BuildContext After Await

```dart
// CRITICAL — always check mounted after any await in StatefulWidget
Future<void> _handleSubmit() async {
  setState(() => _isLoading = true);
  try {
    await authService.login(_email, _password);
    if (!mounted) return; // ← guard before using context
    context.go('/home');
  } on AuthException catch (e) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.message)));
  } finally {
    if (mounted) setState(() => _isLoading = false);
  }
}
```

---

### 4. Widget Architecture

#### Extract to Classes, Not Methods

```dart
// BAD — private method returning widget, prevents optimization
Widget _buildHeader() {
  return Container(
    padding: const EdgeInsets.all(16),
    child: Text(title, style: Theme.of(context).textTheme.headlineMedium),
  );
}

// GOOD — separate widget class, enables const, element reuse
class _PageHeader extends StatelessWidget {
  const _PageHeader(this.title);
  final String title;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Text(title, style: Theme.of(context).textTheme.headlineMedium),
    );
  }
}
```

#### const Propagation

```dart
// BAD — new instances every rebuild
child: Padding(
  padding: EdgeInsets.all(16.0),       // not const
  child: Icon(Icons.home, size: 24.0), // not const
)

// GOOD — const stops rebuild propagation
child: const Padding(
  padding: EdgeInsets.all(16.0),
  child: Icon(Icons.home, size: 24.0),
)
```

#### Scoped Rebuilds

```dart
// BAD — entire page rebuilds on every counter change
class CounterPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider); // rebuilds everything
    return Scaffold(
      body: Column(children: [
        const ExpensiveHeader(), // unnecessarily rebuilt
        Text('$count'),
        const ExpensiveFooter(), // unnecessarily rebuilt
      ]),
    );
  }
}

// GOOD — isolate the rebuilding part
class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Column(children: [
        ExpensiveHeader(),        // never rebuilt (const)
        _CounterDisplay(),        // only this rebuilds
        ExpensiveFooter(),        // never rebuilt (const)
      ]),
    );
  }
}

class _CounterDisplay extends ConsumerWidget {
  const _CounterDisplay();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

---

### 5. State Management: BLoC/Cubit

```dart
// Cubit — synchronous or simple async state
class AuthCubit extends Cubit<AuthState> {
  AuthCubit(this._authService) : super(const AuthState.initial());
  final AuthService _authService;

  Future<void> login(String email, String password) async {
    emit(const AuthState.loading());
    try {
      final user = await _authService.login(email, password);
      emit(AuthState.authenticated(user));
    } on AuthException catch (e) {
      emit(AuthState.error(e.message));
    }
  }

  void logout() {
    _authService.logout();
    emit(const AuthState.initial());
  }
}

// In widget
BlocBuilder<AuthCubit, AuthState>(
  builder: (context, state) => switch (state) {
    AuthInitial() => const LoginForm(),
    AuthLoading() => const CircularProgressIndicator(),
    AuthAuthenticated(:final user) => HomePage(user: user),
    AuthError(:final message) => ErrorView(message: message),
  },
)
```

---

### 6. State Management: Riverpod

```dart
// Auto-dispose async provider
@riverpod
Future<List<Product>> products(Ref ref) async {
  final repo = ref.watch(productRepositoryProvider);
  return repo.getAll();
}

// Notifier with complex mutations
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  List<CartItem> build() => [];

  void add(Product product) {
    final existing = state.where((i) => i.productId == product.id).firstOrNull;
    if (existing != null) {
      state = [
        for (final item in state)
          if (item.productId == product.id) item.copyWith(quantity: item.quantity + 1)
          else item,
      ];
    } else {
      state = [...state, CartItem(productId: product.id, quantity: 1)];
    }
  }

  void remove(String productId) =>
      state = state.where((i) => i.productId != productId).toList();

  void clear() => state = [];
}

// Derived provider (selector pattern)
@riverpod
int cartCount(Ref ref) => ref.watch(cartNotifierProvider).length;

@riverpod
double cartTotal(Ref ref) {
  final cart = ref.watch(cartNotifierProvider);
  final products = ref.watch(productsProvider).valueOrNull ?? [];
  return cart.fold(0.0, (total, item) {
    // firstWhereOrNull (from collection package) avoids StateError when product is missing
    final product = products.firstWhereOrNull((p) => p.id == item.productId);
    return total + (product?.price ?? 0) * item.quantity;
  });
}
```

---

### 7. Navigation with GoRouter

```dart
final router = GoRouter(
  initialLocation: '/',
  // refreshListenable re-evaluates redirect whenever auth state changes
  refreshListenable: GoRouterRefreshStream(authCubit.stream),
  redirect: (context, state) {
    final isLoggedIn = context.read<AuthCubit>().state is AuthAuthenticated;
    final isGoingToLogin = state.matchedLocation == '/login';
    if (!isLoggedIn && !isGoingToLogin) return '/login';
    if (isLoggedIn && isGoingToLogin) return '/';
    return null;
  },
  routes: [
    GoRoute(path: '/login', builder: (_, __) => const LoginPage()),
    ShellRoute(
      builder: (context, state, child) => AppShell(child: child),
      routes: [
        GoRoute(path: '/', builder: (_, __) => const HomePage()),
        GoRoute(
          path: '/products/:id',
          builder: (context, state) =>
              ProductDetailPage(id: state.pathParameters['id']!),
        ),
      ],
    ),
  ],
);
```

---

### 8. HTTP with Dio

```dart
final dio = Dio(BaseOptions(
  baseUrl: const String.fromEnvironment('API_URL'),
  connectTimeout: const Duration(seconds: 10),
  receiveTimeout: const Duration(seconds: 30),
  headers: {'Content-Type': 'application/json'},
));

// Add auth interceptor
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) async {
    final token = await secureStorage.read(key: 'auth_token');
    if (token != null) options.headers['Authorization'] = 'Bearer $token';
    handler.next(options);
  },
  onError: (error, handler) async {
    // Guard against infinite retry loops: only attempt refresh once per request
    final isRetry = error.requestOptions.extra['_isRetry'] == true;
    if (!isRetry && error.response?.statusCode == 401) {
      final refreshed = await attemptTokenRefresh();
      if (refreshed) {
        error.requestOptions.extra['_isRetry'] = true;
        return handler.resolve(await dio.fetch(error.requestOptions));
      }
    }
    handler.next(error);
  },
));

// Repository using Dio
class UserApiDataSource {
  const UserApiDataSource(this._dio);
  final Dio _dio;

  Future<User> getById(String id) async {
    final response = await _dio.get<Map<String, dynamic>>('/users/$id');
    return User.fromJson(response.data!);
  }
}
```

---

### 9. Error Handling Architecture

```dart
// Global error capture — set up in main()
void main() {
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    crashlytics.recordFlutterFatalError(details);
  };

  PlatformDispatcher.instance.onError = (error, stack) {
    crashlytics.recordError(error, stack, fatal: true);
    return true;
  };

  runApp(const App());
}

// Custom ErrorWidget for production
class App extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    ErrorWidget.builder = (details) => ProductionErrorWidget(details);
    return MaterialApp.router(routerConfig: router);
  }
}
```

---

### 10. Testing Quick Reference

```dart
// Unit test — use case
test('GetUserUseCase returns null for missing user', () async {
  final repo = FakeUserRepository();
  final useCase = GetUserUseCase(repo);
  expect(await useCase('missing-id'), isNull);
});

// BLoC test
blocTest<AuthCubit, AuthState>(
  'emits loading then error on failed login',
  build: () => AuthCubit(FakeAuthService(throwsOn: 'login')),
  act: (cubit) => cubit.login('user@test.com', 'wrong'),
  expect: () => [const AuthState.loading(), isA<AuthError>()],
);

// Widget test
testWidgets('CartBadge shows item count', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [cartNotifierProvider.overrideWith(() => FakeCartNotifier(count: 3))],
      child: const MaterialApp(home: CartBadge()),
    ),
  );
  expect(find.text('3'), findsOneWidget);
});
```

---

### References

- [Effective Dart: Design](https://dart.dev/effective-dart/design)
- [Flutter Performance Best Practices](https://docs.flutter.dev/perf/best-practices)
- [Riverpod Documentation](https://riverpod.dev/)
- [BLoC Library](https://bloclibrary.dev/)
- [GoRouter](https://pub.dev/packages/go_router)
- [Freezed](https://pub.dev/packages/freezed)
- Skill: `languages:dart` (`references/review.md`) — comprehensive review checklist
- Rules: `rules/dart/` — coding style, patterns, security, testing, hooks

## Dart and Flutter

<!-- source: github/awesome-copilot instructions/dart-n-flutter.instructions.md -->

Best practices recommended by the Dart and Flutter teams. These instructions were taken from [Effective Dart](https://dart.dev/effective-dart) and [Architecture Recommendations](https://docs.flutter.dev/app-architecture/recommendations).

### Effective Dart

Over the past several years, we've written a ton of Dart code and learned a lot about what works well and what doesn't. We're sharing this with you so you can write consistent, robust, fast code too. There are two overarching themes:

1.  **Be consistent.** When it comes to things like formatting, and casing, arguments about which is better are subjective and impossible to resolve. What we do know is that being *consistent* is objectively helpful.

    If two pieces of code look different it should be because they *are* different in some meaningful way. When a bit of code stands out and catches your eye, it should do so for a useful reason.

2.  **Be brief.** Dart was designed to be familiar, so it inherits many of the same statements and expressions as C, Java, JavaScript and other languages. But we created Dart because there is a lot of room to improve on what those languages offer. We added a bunch of features, from string interpolation to initializing formals, to help you express your intent more simply and easily.

    If there are multiple ways to say something, you should generally pick the most concise one. This is not to say you should `code golf` yourself into cramming a whole program into a single line. The goal is code that is *economical*, not *dense*.

#### The topics

We split the guidelines into a few separate topics for easy digestion:

*   **Style** – This defines the rules for laying out and organizing code, or at least the parts that `dart format` doesn't handle for you. The style topic also specifies how identifiers are formatted: `camelCase`, `using_underscores`, etc.

*   **Documentation** – This tells you everything you need to know about what goes inside comments. Both doc comments and regular, run-of-the-mill code comments.

*   **Usage** – This teaches you how to make the best use of language features to implement behavior. If it's in a statement or expression, it's covered here.

*   **Design** – This is the softest topic, but the one with the widest scope. It covers what we've learned about designing consistent, usable APIs for libraries. If it's in a type signature or declaration, this goes over it.

#### How to read the topics

Each topic is broken into a few sections. Sections contain a list of guidelines. Each guideline starts with one of these words:

*   **DO** guidelines describe practices that should always be followed. There will almost never be a valid reason to stray from them.

*   **DON'T** guidelines are the converse: things that are almost never a good idea. Hopefully, we don't have as many of these as other languages do because we have less historical baggage.

*   **PREFER** guidelines are practices that you *should* follow. However, there may be circumstances where it makes sense to do otherwise. Just make sure you understand the full implications of ignoring the guideline when you do.

*   **AVOID** guidelines are the dual to "prefer": stuff you shouldn't do but where there may be good reasons to on rare occasions.

*   **CONSIDER** guidelines are practices that you might or might not want to follow, depending on circumstances, precedents, and your own preference.

Some guidelines describe an **exception** where the rule does *not* apply. When listed, the exceptions may not be exhaustive—you might still need to use your judgement on other cases.

This sounds like the police are going to beat down your door if you don't have your laces tied correctly. Things aren't that bad. Most of the guidelines here are common sense and we're all reasonable people. The goal, as always, is nice, readable and maintainable code.

#### Rules

##### Style

###### Identifiers

*   DO name types using `UpperCamelCase`.
*   DO name extensions using `UpperCamelCase`.
*   DO name packages, directories, and source files using `lowercase_with_underscores`.
*   DO name import prefixes using `lowercase_with_underscores`.
*   DO name other identifiers using `lowerCamelCase`.
*   PREFER using `lowerCamelCase` for constant names.
*   DO capitalize acronyms and abbreviations longer than two letters like words.
*   PREFER using wildcards for unused callback parameters.
*   DON'T use a leading underscore for identifiers that aren't private.
*   DON'T use prefix letters.
*   DON'T explicitly name libraries.

###### Ordering

*   DO place `dart:` imports before other imports.
*   DO place `package:` imports before relative imports.
*   DO specify exports in a separate section after all imports.
*   DO sort sections alphabetically.

###### Formatting

*   DO format your code using `dart format`.
*   CONSIDER changing your code to make it more formatter-friendly.
*   PREFER lines 80 characters or fewer.
*   DO use curly braces for all flow control statements.

##### Documentation

###### Comments

*   DO format comments like sentences.
*   DON'T use block comments for documentation.

###### Doc comments

*   DO use `///` doc comments to document members and types.
*   PREFER writing doc comments for public APIs.
*   CONSIDER writing a library-level doc comment.
*   CONSIDER writing doc comments for private APIs.
*   DO start doc comments with a single-sentence summary.
*   DO separate the first sentence of a doc comment into its own paragraph.
*   AVOID redundancy with the surrounding context.
*   PREFER starting comments of a function or method with third-person verbs if its main purpose is a side effect.
*   PREFER starting a non-boolean variable or property comment with a noun phrase.
*   PREFER starting a boolean variable or property comment with "Whether" followed by a noun or gerund phrase.
*   PREFER a noun phrase or non-imperative verb phrase for a function or method if returning a value is its primary purpose.
*   DON'T write documentation for both the getter and setter of a property.
*   PREFER starting library or type comments with noun phrases.
*   CONSIDER including code samples in doc comments.
*   DO use square brackets in doc comments to refer to in-scope identifiers.
*   DO use prose to explain parameters, return values, and exceptions.
*   DO put doc comments before metadata annotations.

###### Markdown

*   AVOID using markdown excessively.
*   AVOID using HTML for formatting.
*   PREFER backtick fences for code blocks.

###### Writing

*   PREFER brevity.
*   AVOID abbreviations and acronyms unless they are obvious.
*   PREFER using "this" instead of "the" to refer to a member's instance.

##### Usage

###### Libraries

*   DO use strings in `part of` directives.
*   DON'T import libraries that are inside the `src` directory of another package.
*   DON'T allow an import path to reach into or out of `lib`.
*   PREFER relative import paths.

###### Null

*   DON'T explicitly initialize variables to `null`.
*   DON'T use an explicit default value of `null`.
*   DON'T use `true` or `false` in equality operations.
*   AVOID `late` variables if you need to check whether they are initialized.
*   CONSIDER type promotion or null-check patterns for using nullable types.

###### Strings

*   DO use adjacent strings to concatenate string literals.
*   PREFER using interpolation to compose strings and values.
*   AVOID using curly braces in interpolation when not needed.

###### Collections

*   DO use collection literals when possible.
*   DON'T use `.length` to see if a collection is empty.
*   AVOID using `Iterable.forEach()` with a function literal.
*   DON'T use `List.from()` unless you intend to change the type of the result.
*   DO use `whereType()` to filter a collection by type.
*   DON'T use `cast()` when a nearby operation will do.
*   AVOID using `cast()`.

###### Functions

*   DO use a function declaration to bind a function to a name.
*   DON'T create a lambda when a tear-off will do.

###### Variables

*   DO follow a consistent rule for `var` and `final` on local variables.
*   AVOID storing what you can calculate.

###### Members

*   DON'T wrap a field in a getter and setter unnecessarily.
*   PREFER using a `final` field to make a read-only property.
*   CONSIDER using `=>` for simple members.
*   DON'T use `this.` except to redirect to a named constructor or to avoid shadowing.
*   DO initialize fields at their declaration when possible.

###### Constructors

*   DO use initializing formals when possible.
*   DON'T use `late` when a constructor initializer list will do.
*   DO use `;` instead of `{}` for empty constructor bodies.
*   DON'T use `new`.
*   DON'T use `const` redundantly.

###### Error handling

*   AVOID catches without `on` clauses.
*   DON'T discard errors from catches without `on` clauses.
*   DO throw objects that implement `Error` only for programmatic errors.
*   DON'T explicitly catch `Error` or types that implement it.
*   DO use `rethrow` to rethrow a caught exception.

###### Asynchrony

*   PREFER async/await over using raw futures.
*   DON'T use `async` when it has no useful effect.
*   CONSIDER using higher-order methods to transform a stream.
*   AVOID using Completer directly.
*   DO test for `Future<T>` when disambiguating a `FutureOr<T>` whose type argument could be `Object`.

##### Design

###### Names

*   DO use terms consistently.
*   AVOID abbreviations.
*   PREFER putting the most descriptive noun last.
*   CONSIDER making the code read like a sentence.
*   PREFER a noun phrase for a non-boolean property or variable.
*   PREFER a non-imperative verb phrase for a boolean property or variable.
*   CONSIDER omitting the verb for a named boolean parameter.
*   PREFER the "positive" name for a boolean property or variable.
*   PREFER an imperative verb phrase for a function or method whose main purpose is a side effect.
*   PREFER a noun phrase or non-imperative verb phrase for a function or method if returning a value is its primary purpose.
*   CONSIDER an imperative verb phrase for a function or method if you want to draw attention to the work it performs.
*   AVOID starting a method name with `get`.
*   PREFER naming a method `to...()` if it copies the object's state to a new object.
*   PREFER naming a method `as...()` if it returns a different representation backed by the original object.
*   AVOID describing the parameters in the function's or method's name.
*   DO follow existing mnemonic conventions when naming type parameters.

###### Libraries

*   PREFER making declarations private.
*   CONSIDER declaring multiple classes in the same library.

###### Classes and mixins

*   AVOID defining a one-member abstract class when a simple function will do.
*   AVOID defining a class that contains only static members.
*   AVOID extending a class that isn't intended to be subclassed.
*   DO use class modifiers to control if your class can be extended.
*   AVOID implementing a class that isn't intended to be an interface.
*   DO use class modifiers to control if your class can be an interface.
*   PREFER defining a pure `mixin` or pure `class` to a `mixin class`.

###### Constructors

*   CONSIDER making your constructor `const` if the class supports it.

###### Members

*   PREFER making fields and top-level variables `final`.
*   DO use getters for operations that conceptually access properties.
*   DO use setters for operations that conceptually change properties.
*   DON'T define a setter without a corresponding getter.
*   AVOID using runtime type tests to fake overloading.
*   AVOID public `late final` fields without initializers.
*   AVOID returning nullable `Future`, `Stream`, and collection types.
*   AVOID returning `this` from methods just to enable a fluent interface.

###### Types

*   DO type annotate variables without initializers.
*   DO type annotate fields and top-level variables if the type isn't obvious.
*   DON'T redundantly type annotate initialized local variables.
*   DO annotate return types on function declarations.
*   DO annotate parameter types on function declarations.
*   DON'T annotate inferred parameter types on function expressions.
*   DON'T type annotate initializing formals.
*   DO write type arguments on generic invocations that aren't inferred.
*   DON'T write type arguments on generic invocations that are inferred.
*   AVOID writing incomplete generic types.
*   DO annotate with `dynamic` instead of letting inference fail.
*   PREFER signatures in function type annotations.
*   DON'T specify a return type for a setter.
*   DON'T use the legacy typedef syntax.
*   PREFER inline function types over typedefs.
*   PREFER using function type syntax for parameters.
*   AVOID using `dynamic` unless you want to disable static checking.
*   DO use `Future<void>` as the return type of asynchronous members that do not produce values.
*   AVOID using `FutureOr<T>` as a return type.

###### Parameters

*   AVOID positional boolean parameters.
*   AVOID optional positional parameters if the user may want to omit earlier parameters.
*   AVOID mandatory parameters that accept a special "no argument" value.
*   DO use inclusive start and exclusive end parameters to accept a range.

###### Equality

*   DO override `hashCode` if you override `==`.
*   DO make your `==` operator obey the mathematical rules of equality.
*   AVOID defining custom equality for mutable classes.
*   DON'T make the parameter to `==` nullable.

---

### Flutter Architecture Recommendations

This page presents architecture best practices, why they matter, and
whether we recommend them for your Flutter application.
You should treat these recommendations as recommendations,
and not steadfast rules, and you should
adapt them to your app's unique requirements.

The best practices on this page have a priority,
which reflects how strongly the Flutter team recommends it.

* **Strongly recommend:** You should always implement this recommendation if
  you're starting to build a new application. You should strongly consider
  refactoring an existing app to implement this practice unless doing so would
  fundamentally clash with your current approach.
* **Recommend**: This practice will likely improve your app.
* **Conditional**: This practice can improve your app in certain circumstances.

#### Separation of concerns

You should separate your app into a UI layer and a data layer. Within those layers, you should further separate logic into classes by responsibility.

##### Use clearly defined data and UI layers.
**Strongly recommend**

Separation of concerns is the most important architectural principle.
The data layer exposes application data to the rest of the app, and contains most of the business logic in your application.
The UI layer displays application data and listens for user events from users. The UI layer contains separate classes for UI logic and widgets.

##### Use the repository pattern in the data layer.
**Strongly recommend**

The repository pattern is a software design pattern that isolates the data access logic from the rest of the application.
It creates an abstraction layer between the application's business logic and the underlying data storage mechanisms (databases, APIs, file systems, etc.).
In practice, this means creating Repository classes and Service classes.

##### Use ViewModels and Views in the UI layer. (MVVM)
**Strongly recommend**

Separation of concerns is the most important architectural principle.
This particular separation makes your code much less error prone because your widgets remain "dumb".

##### Use `ChangeNotifiers` and `Listenables` to handle widget updates.
**Conditional**

> There are many options to handle state-management, and ultimately the decision comes down to personal preference.

The `ChangeNotifier` API is part of the Flutter SDK, and is a convenient way to have your widgets observe changes in your ViewModels.

##### Do not put logic in widgets.
**Strongly recommend**

Logic should be encapsulated in methods on the ViewModel. The only logic a view should contain is:
* Simple if-statements to show and hide widgets based on a flag or nullable field in the ViewModel
* Animation logic that relies on the widget to calculate
* Layout logic based on device information, like screen size or orientation.
* Simple routing logic

##### Use a domain layer.
**Conditional**

> Use in apps with complex logic requirements.

A domain layer is only needed if your application has exceeding complex logic that crowds your ViewModels,
or if you find yourself repeating logic in ViewModels.
In very large apps, use-cases are useful, but in most apps they add unnecessary overhead.

#### Handling data

Handling data with care makes your code easier to understand, less error prone, and
prevents malformed or unexpected data from being created.

##### Use unidirectional data flow.
**Strongly recommend**

Data updates should only flow from the data layer to the UI layer.
Interactions in the UI layer are sent to the data layer where they're processed.

##### Use `Commands` to handle events from user interaction.
**Recommend**

Commands prevent rendering errors in your app, and standardize how the UI layer sends events to the data layer.

##### Use immutable data models.
**Strongly recommend**

Immutable data is crucial in ensuring that any necessary changes occur only in the proper place, usually the data or domain layer.
Because immutable objects can't be modified after creation, you must create a new instance to reflect changes.
This process prevents accidental updates in the UI layer and supports a clear, unidirectional data flow.

##### Use freezed or built_value to generate immutable data models.
**Recommend**

You can use packages to help generate useful functionality in your data models, `freezed` or `built_value`.
These can generate common model methods like JSON ser/des, deep equality checking and copy methods.
These code generation packages can add significant build time to your applications if you have a lot of models.

##### Create separate API models and domain models.
**Conditional**

> Use in large apps.

Using separate models adds verbosity, but prevents complexity in ViewModels and use-cases.

#### App structure

Well organized code benefits both the health of the app itself, and the team working on the code.

##### Use dependency injection.
**Strongly recommend**

Dependency injection prevents your app from having globally accessible objects, which makes your code less error prone.
We recommend you use the `provider` package to handle dependency injection.

##### Use `go_router` for navigation.
**Recommend**

Go_router is the preferred way to write 90% of Flutter applications.
There are some specific use-cases that go_router doesn't solve,
in which case you can use the `Flutter Navigator API` directly or try other packages found on `pub.dev`.

##### Use standardized naming conventions for classes, files and directories.
**Recommend**

We recommend naming classes for the architectural component they represent.
For example, you may have the following classes:

* HomeViewModel
* HomeScreen
* UserRepository
* ClientApiService

For clarity, we do not recommend using names that can be confused with objects from the Flutter SDK.
For example, you should put your shared widgets in a directory called `ui/core/`,
rather than a directory called `/widgets`.

##### Use abstract repository classes
**Strongly recommend**

Repository classes are the sources of truth for all data in your app,
and facilitate communication with external APIs.
Creating abstract repository classes allows you to create different implementations,
which can be used for different app environments, such as "development" and "staging".

#### Testing

Good testing practices makes your app flexible.
It also makes it straightforward and low risk to add new logic and new UI.

##### Test architectural components separately, and together.
**Strongly recommend**

* Write unit tests for every service, repository and ViewModel class. These tests should test the logic of every method individually.
* Write widget tests for views. Testing routing and dependency injection are particularly important.

##### Make fakes for testing (and write code that takes advantage of fakes.)
**Strongly recommend**

Fakes aren't concerned with the inner workings of any given method as much
as they're concerned with inputs and outputs. If you have this in mind while writing application code,
you're forced to write modular, lightweight functions and classes with well defined inputs and outputs.
