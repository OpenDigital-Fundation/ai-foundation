# Java and Kotlin — spring-boot

Part of `languages:jvm`. Load only when the project uses spring-boot.

## Spring Boot Development Patterns

<!-- source: affaan-m/ECC pi/core/skills/springboot-patterns/SKILL.md -->

Spring Boot architecture and API patterns for scalable, production-grade services.

### When to Activate

- Building REST APIs with Spring MVC or WebFlux
- Structuring controller → service → repository layers
- Configuring Spring Data JPA, caching, or async processing
- Adding validation, exception handling, or pagination
- Setting up profiles for dev/staging/production environments
- Implementing event-driven patterns with Spring Events or Kafka

### REST API Structure

```java
@RestController
@RequestMapping("/api/markets")
@Validated
class MarketController {
  private final MarketService marketService;

  MarketController(MarketService marketService) {
    this.marketService = marketService;
  }

  @GetMapping
  ResponseEntity<Page<MarketResponse>> list(
      @RequestParam(defaultValue = "0") int page,
      @RequestParam(defaultValue = "20") int size) {
    Page<Market> markets = marketService.list(PageRequest.of(page, size));
    return ResponseEntity.ok(markets.map(MarketResponse::from));
  }

  @PostMapping
  ResponseEntity<MarketResponse> create(@Valid @RequestBody CreateMarketRequest request) {
    Market market = marketService.create(request);
    return ResponseEntity.status(HttpStatus.CREATED).body(MarketResponse.from(market));
  }
}
```

### Repository Pattern (Spring Data JPA)

```java
public interface MarketRepository extends JpaRepository<MarketEntity, Long> {
  @Query("select m from MarketEntity m where m.status = :status order by m.volume desc")
  List<MarketEntity> findActive(@Param("status") MarketStatus status, Pageable pageable);
}
```

### Service Layer with Transactions

```java
@Service
public class MarketService {
  private final MarketRepository repo;

  public MarketService(MarketRepository repo) {
    this.repo = repo;
  }

  @Transactional
  public Market create(CreateMarketRequest request) {
    MarketEntity entity = MarketEntity.from(request);
    MarketEntity saved = repo.save(entity);
    return Market.from(saved);
  }
}
```

### DTOs and Validation

```java
public record CreateMarketRequest(
    @NotBlank @Size(max = 200) String name,
    @NotBlank @Size(max = 2000) String description,
    @NotNull @FutureOrPresent Instant endDate,
    @NotEmpty List<@NotBlank String> categories) {}

public record MarketResponse(Long id, String name, MarketStatus status) {
  static MarketResponse from(Market market) {
    return new MarketResponse(market.id(), market.name(), market.status());
  }
}
```

### Exception Handling

```java
@ControllerAdvice
class GlobalExceptionHandler {
  @ExceptionHandler(MethodArgumentNotValidException.class)
  ResponseEntity<ApiError> handleValidation(MethodArgumentNotValidException ex) {
    String message = ex.getBindingResult().getFieldErrors().stream()
        .map(e -> e.getField() + ": " + e.getDefaultMessage())
        .collect(Collectors.joining(", "));
    return ResponseEntity.badRequest().body(ApiError.validation(message));
  }

  @ExceptionHandler(AccessDeniedException.class)
  ResponseEntity<ApiError> handleAccessDenied() {
    return ResponseEntity.status(HttpStatus.FORBIDDEN).body(ApiError.of("Forbidden"));
  }

  @ExceptionHandler(Exception.class)
  ResponseEntity<ApiError> handleGeneric(Exception ex) {
    // Log unexpected errors with stack traces
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
        .body(ApiError.of("Internal server error"));
  }
}
```

### Caching

Requires `@EnableCaching` on a configuration class.

```java
@Service
public class MarketCacheService {
  private final MarketRepository repo;

  public MarketCacheService(MarketRepository repo) {
    this.repo = repo;
  }

  @Cacheable(value = "market", key = "#id")
  public Market getById(Long id) {
    return repo.findById(id)
        .map(Market::from)
        .orElseThrow(() -> new EntityNotFoundException("Market not found"));
  }

  @CacheEvict(value = "market", key = "#id")
  public void evict(Long id) {}
}
```

### Async Processing

Requires `@EnableAsync` on a configuration class.

```java
@Service
public class NotificationService {
  @Async
  public CompletableFuture<Void> sendAsync(Notification notification) {
    // send email/SMS
    return CompletableFuture.completedFuture(null);
  }
}
```

### Logging (SLF4J)

```java
@Service
public class ReportService {
  private static final Logger log = LoggerFactory.getLogger(ReportService.class);

  public Report generate(Long marketId) {
    log.info("generate_report marketId={}", marketId);
    try {
      // logic
    } catch (Exception ex) {
      log.error("generate_report_failed marketId={}", marketId, ex);
      throw ex;
    }
    return new Report();
  }
}
```

### Middleware / Filters

```java
@Component
public class RequestLoggingFilter extends OncePerRequestFilter {
  private static final Logger log = LoggerFactory.getLogger(RequestLoggingFilter.class);

  @Override
  protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
      FilterChain filterChain) throws ServletException, IOException {
    long start = System.currentTimeMillis();
    try {
      filterChain.doFilter(request, response);
    } finally {
      long duration = System.currentTimeMillis() - start;
      log.info("req method={} uri={} status={} durationMs={}",
          request.getMethod(), request.getRequestURI(), response.getStatus(), duration);
    }
  }
}
```

### Pagination and Sorting

```java
PageRequest page = PageRequest.of(pageNumber, pageSize, Sort.by("createdAt").descending());
Page<Market> results = marketService.list(page);
```

### Error-Resilient External Calls

```java
public <T> T withRetry(Supplier<T> supplier, int maxRetries) {
  int attempts = 0;
  while (true) {
    try {
      return supplier.get();
    } catch (Exception ex) {
      attempts++;
      if (attempts >= maxRetries) {
        throw ex;
      }
      try {
        Thread.sleep((long) Math.pow(2, attempts) * 100L);
      } catch (InterruptedException ie) {
        Thread.currentThread().interrupt();
        throw ex;
      }
    }
  }
}
```

### Rate Limiting (Filter + Bucket4j)

**Security Note**: The `X-Forwarded-For` header is untrusted by default because clients can spoof it.
Only use forwarded headers when:
1. Your app is behind a trusted reverse proxy (nginx, AWS ALB, etc.)
2. You have registered `ForwardedHeaderFilter` as a bean
3. You have configured `server.forward-headers-strategy=NATIVE` or `FRAMEWORK` in application properties
4. Your proxy is configured to overwrite (not append to) the `X-Forwarded-For` header

When `ForwardedHeaderFilter` is properly configured, `request.getRemoteAddr()` will automatically
return the correct client IP from the forwarded headers. Without this configuration, use
`request.getRemoteAddr()` directly—it returns the immediate connection IP, which is the only
trustworthy value.

```java
@Component
public class RateLimitFilter extends OncePerRequestFilter {
  private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

  /*
   * SECURITY: This filter uses request.getRemoteAddr() to identify clients for rate limiting.
   *
   * If your application is behind a reverse proxy (nginx, AWS ALB, etc.), you MUST configure
   * Spring to handle forwarded headers properly for accurate client IP detection:
   *
   * 1. Set server.forward-headers-strategy=NATIVE (for cloud platforms) or FRAMEWORK in
   *    application.properties/yaml
   * 2. If using FRAMEWORK strategy, register ForwardedHeaderFilter:
   *
   *    @Bean
   *    ForwardedHeaderFilter forwardedHeaderFilter() {
   *        return new ForwardedHeaderFilter();
   *    }
   *
   * 3. Ensure your proxy overwrites (not appends) the X-Forwarded-For header to prevent spoofing
   * 4. Configure server.tomcat.remoteip.trusted-proxies or equivalent for your container
   *
   * Without this configuration, request.getRemoteAddr() returns the proxy IP, not the client IP.
   * Do NOT read X-Forwarded-For directly—it is trivially spoofable without trusted proxy handling.
   */
  @Override
  protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
      FilterChain filterChain) throws ServletException, IOException {
    // Use getRemoteAddr() which returns the correct client IP when ForwardedHeaderFilter
    // is configured, or the direct connection IP otherwise. Never trust X-Forwarded-For
    // headers directly without proper proxy configuration.
    String clientIp = request.getRemoteAddr();

    Bucket bucket = buckets.computeIfAbsent(clientIp,
        k -> Bucket.builder()
            .addLimit(Bandwidth.classic(100, Refill.greedy(100, Duration.ofMinutes(1))))
            .build());

    if (bucket.tryConsume(1)) {
      filterChain.doFilter(request, response);
    } else {
      response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
    }
  }
}
```

### Background Jobs

Use Spring’s `@Scheduled` or integrate with queues (e.g., Kafka, SQS, RabbitMQ). Keep handlers idempotent and observable.

### Observability

- Structured logging (JSON) via Logback encoder
- Metrics: Micrometer + Prometheus/OTel
- Tracing: Micrometer Tracing with OpenTelemetry or Brave backend

### Production Defaults

- Prefer constructor injection, avoid field injection
- Enable `spring.mvc.problemdetails.enabled=true` for RFC 7807 errors (Spring Boot 3+)
- Configure HikariCP pool sizes for workload, set timeouts
- Use `@Transactional(readOnly = true)` for queries
- Enforce null-safety via `@NonNull` and `Optional` where appropriate

**Remember**: Keep controllers thin, services focused, repositories simple, and errors handled centrally. Optimize for maintainability and testability.

## Spring Boot TDD Workflow

<!-- source: affaan-m/ECC pi/core/skills/springboot-tdd/SKILL.md -->

TDD guidance for Spring Boot services with 80%+ coverage (unit + integration).

### When to Use

- New features or endpoints
- Bug fixes or refactors
- Adding data access logic or security rules

### Workflow

1) Write tests first (they should fail)
2) Implement minimal code to pass
3) Refactor with tests green
4) Enforce coverage (JaCoCo)

### Unit Tests (JUnit 5 + Mockito)

```java
@ExtendWith(MockitoExtension.class)
class MarketServiceTest {
  @Mock MarketRepository repo;
  @InjectMocks MarketService service;

  @Test
  void createsMarket() {
    CreateMarketRequest req = new CreateMarketRequest("name", "desc", Instant.now(), List.of("cat"));
    when(repo.save(any())).thenAnswer(inv -> inv.getArgument(0));

    Market result = service.create(req);

    assertThat(result.name()).isEqualTo("name");
    verify(repo).save(any());
  }
}
```

Patterns:
- Arrange-Act-Assert
- Avoid partial mocks; prefer explicit stubbing
- Use `@ParameterizedTest` for variants

### Web Layer Tests (MockMvc)

```java
@WebMvcTest(MarketController.class)
class MarketControllerTest {
  @Autowired MockMvc mockMvc;
  @MockBean MarketService marketService;

  @Test
  void returnsMarkets() throws Exception {
    when(marketService.list(any())).thenReturn(Page.empty());

    mockMvc.perform(get("/api/markets"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.content").isArray());
  }
}
```

### Integration Tests (SpringBootTest)

```java
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class MarketIntegrationTest {
  @Autowired MockMvc mockMvc;

  @Test
  void createsMarket() throws Exception {
    mockMvc.perform(post("/api/markets")
        .contentType(MediaType.APPLICATION_JSON)
        .content("""
          {"name":"Test","description":"Desc","endDate":"2030-01-01T00:00:00Z","categories":["general"]}
        """))
      .andExpect(status().isCreated());
  }
}
```

### Persistence Tests (DataJpaTest)

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Import(TestContainersConfig.class)
class MarketRepositoryTest {
  @Autowired MarketRepository repo;

  @Test
  void savesAndFinds() {
    MarketEntity entity = new MarketEntity();
    entity.setName("Test");
    repo.save(entity);

    Optional<MarketEntity> found = repo.findByName("Test");
    assertThat(found).isPresent();
  }
}
```

### Testcontainers

- Use reusable containers for Postgres/Redis to mirror production
- Wire via `@DynamicPropertySource` to inject JDBC URLs into Spring context

### Coverage (JaCoCo)

Maven snippet:
```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.14</version>
  <executions>
    <execution>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

### Assertions

- Prefer AssertJ (`assertThat`) for readability
- For JSON responses, use `jsonPath`
- For exceptions: `assertThatThrownBy(...)`

### Test Data Builders

```java
class MarketBuilder {
  private String name = "Test";
  MarketBuilder withName(String name) { this.name = name; return this; }
  Market build() { return new Market(null, name, MarketStatus.ACTIVE); }
}
```

### CI Commands

- Maven: `mvn -T 4 test` or `mvn verify`
- Gradle: `./gradlew test jacocoTestReport`

**Remember**: Keep tests fast, isolated, and deterministic. Test behavior, not implementation details.

## Spring Boot Security Review

<!-- source: affaan-m/ECC pi/core/skills/springboot-security/SKILL.md -->

Use when adding auth, handling input, creating endpoints, or dealing with secrets.

### When to Activate

- Adding authentication (JWT, OAuth2, session-based)
- Implementing authorization (@PreAuthorize, role-based access)
- Validating user input (Bean Validation, custom validators)
- Configuring CORS, CSRF, or security headers
- Managing secrets (Vault, environment variables)
- Adding rate limiting or brute-force protection
- Scanning dependencies for CVEs

### Authentication

- Prefer stateless JWT or opaque tokens with revocation list
- Use `httpOnly`, `Secure`, `SameSite=Strict` cookies for sessions
- Validate tokens with `OncePerRequestFilter` or resource server

```java
@Component
public class JwtAuthFilter extends OncePerRequestFilter {
  private final JwtService jwtService;

  public JwtAuthFilter(JwtService jwtService) {
    this.jwtService = jwtService;
  }

  @Override
  protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
      FilterChain chain) throws ServletException, IOException {
    String header = request.getHeader(HttpHeaders.AUTHORIZATION);
    if (header != null && header.startsWith("Bearer ")) {
      String token = header.substring(7);
      Authentication auth = jwtService.authenticate(token);
      SecurityContextHolder.getContext().setAuthentication(auth);
    }
    chain.doFilter(request, response);
  }
}
```

### Authorization

- Enable method security: `@EnableMethodSecurity`
- Use `@PreAuthorize("hasRole('ADMIN')")` or `@PreAuthorize("@authz.canEdit(#id)")`
- Deny by default; expose only required scopes

```java
@RestController
@RequestMapping("/api/admin")
public class AdminController {

  @PreAuthorize("hasRole('ADMIN')")
  @GetMapping("/users")
  public List<UserDto> listUsers() {
    return userService.findAll();
  }

  @PreAuthorize("@authz.isOwner(#id, authentication)")
  @DeleteMapping("/users/{id}")
  public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
    userService.delete(id);
    return ResponseEntity.noContent().build();
  }
}
```

### Input Validation

- Use Bean Validation with `@Valid` on controllers
- Apply constraints on DTOs: `@NotBlank`, `@Email`, `@Size`, custom validators
- Sanitize any HTML with a whitelist before rendering

```java
// BAD: No validation
@PostMapping("/users")
public User createUser(@RequestBody UserDto dto) {
  return userService.create(dto);
}

// GOOD: Validated DTO
public record CreateUserDto(
    @NotBlank @Size(max = 100) String name,
    @NotBlank @Email String email,
    @NotNull @Min(0) @Max(150) Integer age
) {}

@PostMapping("/users")
public ResponseEntity<UserDto> createUser(@Valid @RequestBody CreateUserDto dto) {
  return ResponseEntity.status(HttpStatus.CREATED)
      .body(userService.create(dto));
}
```

### SQL Injection Prevention

- Use Spring Data repositories or parameterized queries
- For native queries, use `:param` bindings; never concatenate strings

```java
// BAD: String concatenation in native query
@Query(value = "SELECT * FROM users WHERE name = '" + name + "'", nativeQuery = true)

// GOOD: Parameterized native query
@Query(value = "SELECT * FROM users WHERE name = :name", nativeQuery = true)
List<User> findByName(@Param("name") String name);

// GOOD: Spring Data derived query (auto-parameterized)
List<User> findByEmailAndActiveTrue(String email);
```

### Password Encoding

- Always hash passwords with BCrypt or Argon2 — never store plaintext
- Use `PasswordEncoder` bean, not manual hashing

```java
@Bean
public PasswordEncoder passwordEncoder() {
  return new BCryptPasswordEncoder(12); // cost factor 12
}

// In service
public User register(CreateUserDto dto) {
  String hashedPassword = passwordEncoder.encode(dto.password());
  return userRepository.save(new User(dto.email(), hashedPassword));
}
```

### CSRF Protection

- For browser session apps, keep CSRF enabled; include token in forms/headers
- For pure APIs with Bearer tokens, disable CSRF and rely on stateless auth

```java
http
  .csrf(csrf -> csrf.disable())
  .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
```

### Secrets Management

- No secrets in source; load from env or vault
- Keep `application.yml` free of credentials; use placeholders
- Rotate tokens and DB credentials regularly

```yaml
# BAD: Hardcoded in application.yml
spring:
  datasource:
    password: mySecretPassword123

# GOOD: Environment variable placeholder
spring:
  datasource:
    password: ${DB_PASSWORD}

# GOOD: Spring Cloud Vault integration
spring:
  cloud:
    vault:
      uri: https://vault.example.com
      token: ${VAULT_TOKEN}
```

### Security Headers

```java
http
  .headers(headers -> headers
    .contentSecurityPolicy(csp -> csp
      .policyDirectives("default-src 'self'"))
    .frameOptions(HeadersConfigurer.FrameOptionsConfig::sameOrigin)
    .xssProtection(Customizer.withDefaults())
    .referrerPolicy(rp -> rp.policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.NO_REFERRER)));
```

### CORS Configuration

- Configure CORS at the security filter level, not per-controller
- Restrict allowed origins — never use `*` in production

```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
  CorsConfiguration config = new CorsConfiguration();
  config.setAllowedOrigins(List.of("https://app.example.com"));
  config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
  config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
  config.setAllowCredentials(true);
  config.setMaxAge(3600L);

  UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
  source.registerCorsConfiguration("/api/**", config);
  return source;
}

// In SecurityFilterChain:
http.cors(cors -> cors.configurationSource(corsConfigurationSource()));
```

### Rate Limiting

- Apply Bucket4j or gateway-level limits on expensive endpoints
- Log and alert on bursts; return 429 with retry hints

```java
// Using Bucket4j for per-endpoint rate limiting
@Component
public class RateLimitFilter extends OncePerRequestFilter {
  private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

  private Bucket createBucket() {
    return Bucket.builder()
        .addLimit(Bandwidth.classic(100, Refill.intervally(100, Duration.ofMinutes(1))))
        .build();
  }

  @Override
  protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
      FilterChain chain) throws ServletException, IOException {
    String clientIp = request.getRemoteAddr();
    Bucket bucket = buckets.computeIfAbsent(clientIp, k -> createBucket());

    if (bucket.tryConsume(1)) {
      chain.doFilter(request, response);
    } else {
      response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
      response.getWriter().write("{\"error\": \"Rate limit exceeded\"}");
    }
  }
}
```

### Dependency Security

- Run OWASP Dependency Check / Snyk in CI
- Keep Spring Boot and Spring Security on supported versions
- Fail builds on known CVEs

### Logging and PII

- Never log secrets, tokens, passwords, or full PAN data
- Redact sensitive fields; use structured JSON logging

### File Uploads

- Validate size, content type, and extension
- Store outside web root; scan if required

### Checklist Before Release

- [ ] Auth tokens validated and expired correctly
- [ ] Authorization guards on every sensitive path
- [ ] All inputs validated and sanitized
- [ ] No string-concatenated SQL
- [ ] CSRF posture correct for app type
- [ ] Secrets externalized; none committed
- [ ] Security headers configured
- [ ] Rate limiting on APIs
- [ ] Dependencies scanned and up to date
- [ ] Logs free of sensitive data

**Remember**: Deny by default, validate inputs, least privilege, and secure-by-configuration first.

## Spring Boot Verification Loop

<!-- source: affaan-m/ECC pi/core/skills/springboot-verification/SKILL.md -->

Run before PRs, after major changes, and pre-deploy.

### When to Activate

- Before opening a pull request for a Spring Boot service
- After major refactoring or dependency upgrades
- Pre-deployment verification for staging or production
- Running full build → lint → test → security scan pipeline
- Validating test coverage meets thresholds

### Phase 1: Build

```bash
mvn -T 4 clean verify -DskipTests
# or
./gradlew clean assemble -x test
```

If build fails, stop and fix.

### Phase 2: Static Analysis

Maven (common plugins):
```bash
mvn -T 4 spotbugs:check pmd:check checkstyle:check
```

Gradle (if configured):
```bash
./gradlew checkstyleMain pmdMain spotbugsMain
```

### Phase 3: Tests + Coverage

```bash
mvn -T 4 test
mvn jacoco:report   # verify 80%+ coverage
# or
./gradlew test jacocoTestReport
```

Report:
- Total tests, passed/failed
- Coverage % (lines/branches)

#### Unit Tests

Test service logic in isolation with mocked dependencies:

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

  @Mock private UserRepository userRepository;
  @InjectMocks private UserService userService;

  @Test
  void createUser_validInput_returnsUser() {
    var dto = new CreateUserDto("Alice", "alice@example.com");
    var expected = new User(1L, "Alice", "alice@example.com");
    when(userRepository.save(any(User.class))).thenReturn(expected);

    var result = userService.create(dto);

    assertThat(result.name()).isEqualTo("Alice");
    verify(userRepository).save(any(User.class));
  }

  @Test
  void createUser_duplicateEmail_throwsException() {
    var dto = new CreateUserDto("Alice", "existing@example.com");
    when(userRepository.existsByEmail(dto.email())).thenReturn(true);

    assertThatThrownBy(() -> userService.create(dto))
        .isInstanceOf(DuplicateEmailException.class);
  }
}
```

#### Integration Tests with Testcontainers

Test against a real database instead of H2:

```java
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
      .withDatabaseName("testdb");

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
  }

  @Autowired private UserRepository userRepository;

  @Test
  void findByEmail_existingUser_returnsUser() {
    userRepository.save(new User("Alice", "alice@example.com"));

    var found = userRepository.findByEmail("alice@example.com");

    assertThat(found).isPresent();
    assertThat(found.get().getName()).isEqualTo("Alice");
  }
}
```

#### API Tests with MockMvc

Test controller layer with full Spring context:

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

  @Autowired private MockMvc mockMvc;
  @MockBean private UserService userService;

  @Test
  void createUser_validInput_returns201() throws Exception {
    var user = new UserDto(1L, "Alice", "alice@example.com");
    when(userService.create(any())).thenReturn(user);

    mockMvc.perform(post("/api/users")
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
                {"name": "Alice", "email": "alice@example.com"}
                """))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.name").value("Alice"));
  }

  @Test
  void createUser_invalidEmail_returns400() throws Exception {
    mockMvc.perform(post("/api/users")
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
                {"name": "Alice", "email": "not-an-email"}
                """))
        .andExpect(status().isBadRequest());
  }
}
```

### Phase 4: Security Scan

```bash
# Dependency CVEs
mvn org.owasp:dependency-check-maven:check
# or
./gradlew dependencyCheckAnalyze

# Secrets in source
grep -rn "password\s*=\s*\"" src/ --include="*.java" --include="*.yml" --include="*.properties"
grep -rn "sk-\|api_key\|secret" src/ --include="*.java" --include="*.yml"

# Secrets (git history)
git secrets --scan  # if configured
```

#### Common Security Findings

```
# Check for System.out.println (use logger instead)
grep -rn "System\.out\.print" src/main/ --include="*.java"

# Check for raw exception messages in responses
grep -rn "e\.getMessage()" src/main/ --include="*.java"

# Check for wildcard CORS
grep -rn "allowedOrigins.*\*" src/main/ --include="*.java"
```

### Phase 5: Lint/Format (optional gate)

```bash
mvn spotless:apply   # if using Spotless plugin
./gradlew spotlessApply
```

### Phase 6: Diff Review

```bash
git diff --stat
git diff
```

Checklist:
- No debugging logs left (`System.out`, `log.debug` without guards)
- Meaningful errors and HTTP statuses
- Transactions and validation present where needed
- Config changes documented

### Output Template

```
VERIFICATION REPORT
===================
Build:     [PASS/FAIL]
Static:    [PASS/FAIL] (spotbugs/pmd/checkstyle)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (CVE findings: N)
Diff:      [X files changed]

Overall:   [READY / NOT READY]

Issues to Fix:
1. ...
2. ...
```

### Continuous Mode

- Re-run phases on significant changes or every 30–60 minutes in long sessions
- Keep a short loop: `mvn -T 4 test` + spotbugs for quick feedback

**Remember**: Fast feedback beats late surprises. Keep the gate strict—treat warnings as defects in production systems.

## OpenAPI to Application Generator (Spring Boot)

<!-- source: github/awesome-copilot agents/openapi-to-application-java-spring-boot.agent.md -->

You turn OpenAPI 3 specifications into working Spring Boot applications, spec-first: the spec is the source of truth, openapi-generator produces API interfaces and DTOs at build time, and you implement everything else.

### Workflow

1. If the `openapi-to-application-java-spring-boot` skill is installed, follow it for generator configuration, implementation and verification. Otherwise use this fallback:
   - Save the spec as `src/main/resources/openapi/<name>.yaml` and check it (unique `operationId`s, tags, `required` lists, constraints, error responses, `securitySchemes`).
   - Add `org.openapitools:openapi-generator-maven-plugin` (or the Gradle `org.openapi.generator` plugin), pinned to the latest release from Maven Central, with `generatorName=spring`, `interfaceOnly=true`, `requestMappingMode=api_interface`, `useTags=true`, `skipDefaultInterface=true`, `openApiNullable=false`, `documentationProvider=none`, `annotationLibrary=none`, `generateSupportingFiles=false`, and your `apiPackage`/`modelPackage`. For Spring Boot 4 also set `useSpringBoot4=true` and `useJackson3=true`; on Boot 3 omit both. For Boot 3.2+/4 set `useSpringBuiltInValidation=true` so generated interfaces omit type-level `@Validated` and use MVC method validation. On Boot 3.0/3.1 keep it `false` and explicitly map request-parameter `ConstraintViolationException` to HTTP 400 with the declared error body, without blanket-mapping service-layer violations. Add `spring-boot-starter-validation`.
   - Build once, then read the generated `<Tag>Api` interfaces and models (under `target/generated-sources/openapi` or `build/generated/openapi`) before writing code.
   - Implement one `@RestController` per generated `<Tag>Api` (implement the interface, no extra mappings), with logic in `@Service` classes and persistence in entities separate from the DTOs. The interface carries the server base path; do not duplicate it through controller mappings, context paths or proxy rewriting.
   - Add a `@RestControllerAdvice` preserving each operation's declared error status, media type and response schema, including validation failures. Handle `MethodArgumentNotValidException` for bodies and, on Boot 3.2+/4, `HandlerMethodValidationException` for query/path parameters; override the corresponding handlers if extending `ResponseEntityExceptionHandler`. Use RFC 9457 `ProblemDetail` only when the spec declares it; otherwise return the declared error DTO instead of Spring's default validation response. Ask before filling gaps or changing the contract.
   - Write `@WebMvcTest` slices per controller and a `@SpringBootTest` happy path; cover success, not found and invalid input for each operation, including constrained query/path parameters and request bodies, asserting error status, content type and body schema.
   - Run `./mvnw verify` or `./gradlew build`, start the app, and `curl` one endpoint plus `/actuator/health`. Verify a non-root server URL, such as `/v1` with `/pets` exposed at `/v1/pets`, to catch missing or duplicated prefixes.
2. New project: use the `create-spring-boot-java-project` skill if installed, otherwise generate the project with start.spring.io. Existing project: keep its build tool, Spring Boot and Java versions; never upgrade implicitly.
3. If installed, use the `spring-security` skill for security schemes, the `spring-boot-testing` skill (plus `java-testcontainers` for database or broker tests) for tests, and `java-springboot` for general conventions; otherwise apply standard Spring Boot practices.

### Guidelines

- Review the spec first (operationIds, tags, schemas, constraints, errors, security) and ask about ambiguities; fix the spec, not generated code.
- Pin the generator version; use `useSpringBoot4` + `useJackson3` for Boot 4, defaults for Boot 3.
- Generate interfaces and models only; keep controllers thin, logic in services, entities separate from generated DTOs.
- Preserve the spec's error status codes, media types and response schemas, including validation failures. Use RFC 9457 problem details only when declared; ask before changing the contract.
- Never commit generated sources; always build and run the tests before reporting done.

## Spring Boot Development

<!-- source: github/awesome-copilot instructions/springboot.instructions.md -->

Apply these instructions only when the project uses Spring Boot. For Kotlin projects, see `kotlin-springboot`.

### General Instructions

- Make only high confidence suggestions when reviewing code changes.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.

### Spring Boot Instructions

#### Dependency Injection

- Use constructor injection for all required dependencies.
- Declare dependency fields as `private final`.

#### Configuration

- Use `application.properties` or `application.yml` for externalized configuration, matching what the project already uses.
- Environment Profiles: Use Spring profiles for different environments (dev, test, prod)
- Configuration Properties: Use @ConfigurationProperties for type-safe configuration binding
- Secrets Management: Externalize secrets using environment variables or secret management systems

#### Code Organization

- Package Structure: Organize by feature/domain rather than by layer
- Separation of Concerns: Keep controllers thin, services focused, and repositories simple
- Utility Classes: Make utility classes final with private constructors

#### Service Layer

- Place business logic in `@Service`-annotated classes.
- Services should be stateless and testable.
- Inject repositories via the constructor.
- Service method signatures should use domain IDs or DTOs, not expose repository entities directly unless necessary.

#### Logging

- Use SLF4J for all logging (`private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`).
- Do not use concrete implementations (Logback, Log4j2) or `System.out.println()` directly.
- Use parameterized logging: `logger.info("User {} logged in", userId);`.

#### Security & Input Handling

- Use parameterized queries | Always use Spring Data JPA or `NamedParameterJdbcTemplate` to prevent SQL injection.
- Validate request bodies and parameters using Bean Validation (`@Valid`, `@NotNull`, `@Size`, etc.) annotations and handle `MethodArgumentNotValidException` in a `@RestControllerAdvice`

### Build and Verification

- After adding or modifying code, verify the project continues to build successfully.
- If the project uses Maven, run `./mvnw verify` (use the wrapper). `package` skips Failsafe integration tests (`*IT`).
- If the project uses Gradle, run `./gradlew build` (or `gradlew.bat build` on Windows).
- Ensure all tests pass as part of the build.
- Use `package` or `test` only as focused, faster commands, not as the verification gate.

### Useful Commands

| Gradle Command            | Maven Command                     | Description                                   |
|:--------------------------|:----------------------------------|:----------------------------------------------|
| `./gradlew bootRun`       |`./mvnw spring-boot:run`           | Run the application.                          |
| `./gradlew build`         |`./mvnw verify`                    | Build and run all tests.                      |
| `./gradlew test`          |`./mvnw test`                      | Run tests.                                    |
| `./gradlew bootJar`       |`./mvnw spring-boot:repackage`     | Package the application as a JAR.             |
| `./gradlew bootBuildImage`|`./mvnw spring-boot:build-image`   | Package the application as a container image. |
