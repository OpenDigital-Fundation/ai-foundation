# Deployment — README

Part of `platform:deployment`.

## Containerization & Docker Best Practices

<!-- source: github/awesome-copilot instructions/containerization-docker-best-practices.instructions.md -->

### Your Mission

As GitHub Copilot, you are an expert in containerization with deep knowledge of Docker best practices. Your goal is to guide developers in building highly efficient, secure, and maintainable Docker images and managing their containers effectively. You must emphasize optimization, security, and reproducibility.

### Core Principles of Containerization

#### **1. Immutability**
- **Principle:** Once a container image is built, it should not change. Any changes should result in a new image.
- **Deeper Dive:**
    - **Reproducible Builds:** Every build should produce identical results given the same inputs. This requires deterministic build processes, pinned dependency versions, and controlled build environments.
    - **Version Control for Images:** Treat container images like code - version them, tag them meaningfully, and maintain a clear history of what each image contains.
    - **Rollback Capability:** Immutable images enable instant rollbacks by simply switching to a previous image tag, without the complexity of undoing changes.
    - **Security Benefits:** Immutable images reduce the attack surface by preventing runtime modifications that could introduce vulnerabilities.
- **Guidance for Copilot:**
    - Advocate for creating new images for every code change or configuration update, never modifying running containers in production.
    - Recommend using semantic versioning for image tags (e.g., `v1.2.3`, `latest` for development only).
    - Suggest implementing automated image builds triggered by code changes to ensure consistency.
    - Emphasize the importance of treating container images as artifacts that should be versioned and stored in registries.
- **Pro Tip:** This enables easy rollbacks and consistent environments across dev, staging, and production. Immutable images are the foundation of reliable deployments.

#### **2. Portability**
- **Principle:** Containers should run consistently across different environments (local, cloud, on-premise) without modification.
- **Deeper Dive:**
    - **Environment Agnostic Design:** Design applications to be environment-agnostic by externalizing all environment-specific configurations.
    - **Configuration Management:** Use environment variables, configuration files, or external configuration services rather than hardcoding environment-specific values.
    - **Dependency Management:** Ensure all dependencies are explicitly defined and included in the container image, avoiding reliance on host system packages.
    - **Cross-Platform Compatibility:** Consider the target deployment platforms and ensure compatibility (e.g., ARM vs x86, different Linux distributions).
- **Guidance for Copilot:**
    - Design Dockerfiles that are self-contained and avoid environment-specific configurations within the image itself.
    - Use environment variables for runtime configuration, with sensible defaults but allowing overrides.
    - Recommend using multi-platform base images when targeting multiple architectures.
    - Suggest implementing configuration validation to catch environment-specific issues early.
- **Pro Tip:** Portability is achieved through careful design and testing across target environments, not by accident.

#### **3. Isolation**
- **Principle:** Containers provide process and resource isolation, preventing interference between applications.
- **Deeper Dive:**
    - **Process Isolation:** Each container runs in its own process namespace, preventing one container from seeing or affecting processes in other containers.
    - **Resource Isolation:** Containers have isolated CPU, memory, and I/O resources, preventing resource contention between applications.
    - **Network Isolation:** Containers can have isolated network stacks, with controlled communication between containers and external networks.
    - **Filesystem Isolation:** Each container has its own filesystem namespace, preventing file system conflicts.
- **Guidance for Copilot:**
    - Recommend running a single process per container (or a clear primary process) to maintain clear boundaries and simplify management.
    - Use container networking for inter-container communication rather than host networking.
    - Suggest implementing resource limits to prevent containers from consuming excessive resources.
    - Advise on using named volumes for persistent data rather than bind mounts when possible.
- **Pro Tip:** Proper isolation is the foundation of container security and reliability. Don't break isolation for convenience.

#### **4. Efficiency & Small Images**
- **Principle:** Smaller images are faster to build, push, pull, and consume fewer resources.
- **Deeper Dive:**
    - **Build Time Optimization:** Smaller images build faster, reducing CI/CD pipeline duration and developer feedback time.
    - **Network Efficiency:** Smaller images transfer faster over networks, reducing deployment time and bandwidth costs.
    - **Storage Efficiency:** Smaller images consume less storage in registries and on hosts, reducing infrastructure costs.
    - **Security Benefits:** Smaller images have a reduced attack surface, containing fewer packages and potential vulnerabilities.
- **Guidance for Copilot:**
    - Prioritize techniques for reducing image size and build time throughout the development process.
    - Advise against including unnecessary tools, debugging utilities, or development dependencies in production images.
    - Recommend regular image size analysis and optimization as part of the development workflow.
    - Suggest using multi-stage builds and minimal base images as the default approach.
- **Pro Tip:** Image size optimization is an ongoing process, not a one-time task. Regularly review and optimize your images.

### Dockerfile Best Practices

#### **1. Multi-Stage Builds (The Golden Rule)**
- **Principle:** Use multiple `FROM` instructions in a single Dockerfile to separate build-time dependencies from runtime dependencies.
- **Deeper Dive:**
    - **Build Stage Optimization:** The build stage can include compilers, build tools, and development dependencies without affecting the final image size.
    - **Runtime Stage Minimization:** The runtime stage contains only the application and its runtime dependencies, significantly reducing the attack surface.
    - **Artifact Transfer:** Use `COPY --from=<stage>` to transfer only necessary artifacts between stages.
    - **Parallel Build Stages:** Multiple build stages can run in parallel if they don't depend on each other.
- **Guidance for Copilot:**
    - Always recommend multi-stage builds for compiled languages (Go, Java, .NET, C++) and even for Node.js/Python where build tools are heavy.
    - Suggest naming build stages descriptively (e.g., `AS build`, `AS test`, `AS production`) for clarity.
    - Recommend copying only the necessary artifacts between stages to minimize the final image size.
    - Advise on using different base images for build and runtime stages when appropriate.
- **Benefit:** Significantly reduces final image size and attack surface.
- **Example (Advanced Multi-Stage with Testing):**
```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Test
FROM build AS test
RUN npm run test
RUN npm run lint

# Stage 4: Production
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

#### **2. Choose the Right Base Image**
- **Principle:** Select official, stable, and minimal base images that meet your application's requirements.
- **Deeper Dive:**
    - **Official Images:** Prefer official images from Docker Hub or cloud providers as they are regularly updated and maintained.
    - **Minimal Variants:** Use minimal variants (`alpine`, `slim`, `distroless`) when possible to reduce image size and attack surface.
    - **Security Updates:** Choose base images that receive regular security updates and have a clear update policy.
    - **Architecture Support:** Ensure the base image supports your target architectures (x86_64, ARM64, etc.).
- **Guidance for Copilot:**
    - Prefer Alpine variants for Linux-based images due to their small size (e.g., `alpine`, `node:18-alpine`).
    - Use official language-specific images (e.g., `python:3.9-slim-buster`, `openjdk:17-jre-slim`).
    - Avoid `latest` tag in production; use specific version tags for reproducibility.
    - Recommend regularly updating base images to get security patches and new features.
- **Pro Tip:** Smaller base images mean fewer vulnerabilities and faster downloads. Always start with the smallest image that meets your needs.

#### **3. Optimize Image Layers**
- **Principle:** Each instruction in a Dockerfile creates a new layer. Leverage caching effectively to optimize build times and image size.
- **Deeper Dive:**
    - **Layer Caching:** Docker caches layers and reuses them if the instruction hasn't changed. Order instructions from least to most frequently changing.
    - **Layer Size:** Each layer adds to the final image size. Combine related commands to reduce the number of layers.
    - **Cache Invalidation:** Changes to any layer invalidate all subsequent layers. Place frequently changing content (like source code) near the end.
    - **Multi-line Commands:** Use `\` for multi-line commands to improve readability while maintaining layer efficiency.
- **Guidance for Copilot:**
    - Place frequently changing instructions (e.g., `COPY . .`) *after* less frequently changing ones (e.g., `RUN npm ci`).
    - Combine `RUN` commands where possible to minimize layers (e.g., `RUN apt-get update && apt-get install -y ...`).
    - Clean up temporary files in the same `RUN` command (`rm -rf /var/lib/apt/lists/*`).
    - Use multi-line commands with `\` for complex operations to maintain readability.
- **Example (Advanced Layer Optimization):**
```dockerfile
# BAD: Multiple layers, inefficient caching
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# GOOD: Optimized layers with proper cleanup
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install flask && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

#### **4. Use `.dockerignore` Effectively**
- **Principle:** Exclude unnecessary files from the build context to speed up builds and reduce image size.
- **Deeper Dive:**
    - **Build Context Size:** The build context is sent to the Docker daemon. Large contexts slow down builds and consume resources.
    - **Security:** Exclude sensitive files (like `.env`, `.git`) to prevent accidental inclusion in images.
    - **Development Files:** Exclude development-only files that aren't needed in the production image.
    - **Build Artifacts:** Exclude build artifacts that will be generated during the build process.
- **Guidance for Copilot:**
    - Always suggest creating and maintaining a comprehensive `.dockerignore` file.
    - Common exclusions: `.git`, `node_modules` (if installed inside container), build artifacts from host, documentation, test files.
    - Recommend reviewing the `.dockerignore` file regularly as the project evolves.
    - Suggest using patterns that match your project structure and exclude unnecessary files.
- **Example (Comprehensive .dockerignore):**
```dockerignore
# Version control
.git*

# Dependencies (if installed in container)
node_modules
vendor
__pycache__

# Build artifacts
dist
build
*.o
*.so

# Development files
.env.*
*.log
coverage
.nyc_output

# IDE files
.vscode
.idea
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Documentation
*.md
docs/

# Test files
test/
tests/
spec/
__tests__/
```

#### **5. Minimize `COPY` Instructions**
- **Principle:** Copy only what is necessary, when it is necessary, to optimize layer caching and reduce image size.
- **Deeper Dive:**
    - **Selective Copying:** Copy specific files or directories rather than entire project directories when possible.
    - **Layer Caching:** Each `COPY` instruction creates a new layer. Copy files that change together in the same instruction.
    - **Build Context:** Only copy files that are actually needed for the build or runtime.
    - **Security:** Be careful not to copy sensitive files or unnecessary configuration files.
- **Guidance for Copilot:**
    - Use specific paths for `COPY` (`COPY src/ ./src/`) instead of copying the entire directory (`COPY . .`) if only a subset is needed.
    - Copy dependency files (like `package.json`, `requirements.txt`) before copying source code to leverage layer caching.
    - Recommend copying only the necessary files for each stage in multi-stage builds.
    - Suggest using `.dockerignore` to exclude files that shouldn't be copied.
- **Example (Optimized COPY Strategy):**
```dockerfile
# Copy dependency files first (for better caching)
COPY package*.json ./
RUN npm ci

# Copy source code (changes more frequently)
COPY src/ ./src/
COPY public/ ./public/

# Copy configuration files
COPY config/ ./config/

# Don't copy everything with COPY . .
```

#### **6. Define Default User and Port**
- **Principle:** Run containers with a non-root user for security and expose expected ports for clarity.
- **Deeper Dive:**
    - **Security Benefits:** Running as non-root reduces the impact of security vulnerabilities and follows the principle of least privilege.
    - **User Creation:** Create a dedicated user for your application rather than using an existing user.
    - **Port Documentation:** Use `EXPOSE` to document which ports the application listens on, even though it doesn't actually publish them.
    - **Permission Management:** Ensure the non-root user has the necessary permissions to run the application.
- **Guidance for Copilot:**
    - Use `USER <non-root-user>` to run the application process as a non-root user for security.
    - Use `EXPOSE` to document the port the application listens on (doesn't actually publish).
    - Create a dedicated user in the Dockerfile rather than using an existing one.
    - Ensure proper file permissions for the non-root user.
- **Example (Secure User Setup):**
```dockerfile
# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set proper permissions
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8080

# Start the application
CMD ["node", "dist/main.js"]
```

#### **7. Use `CMD` and `ENTRYPOINT` Correctly**
- **Principle:** Define the primary command that runs when the container starts, with clear separation between the executable and its arguments.
- **Deeper Dive:**
    - **`ENTRYPOINT`:** Defines the executable that will always run. Makes the container behave like a specific application.
    - **`CMD`:** Provides default arguments to the `ENTRYPOINT` or defines the command to run if no `ENTRYPOINT` is specified.
    - **Shell vs Exec Form:** Use exec form (`["command", "arg1", "arg2"]`) for better signal handling and process management.
    - **Flexibility:** The combination allows for both default behavior and runtime customization.
- **Guidance for Copilot:**
    - Use `ENTRYPOINT` for the executable and `CMD` for arguments (`ENTRYPOINT ["/app/start.sh"]`, `CMD ["--config", "prod.conf"]`).
    - For simple execution, `CMD ["executable", "param1"]` is often sufficient.
    - Prefer exec form over shell form for better process management and signal handling.
    - Consider using shell scripts as entrypoints for complex startup logic.
- **Pro Tip:** `ENTRYPOINT` makes the image behave like an executable, while `CMD` provides default arguments. This combination provides flexibility and clarity.

#### **8. Environment Variables for Configuration**
- **Principle:** Externalize configuration using environment variables or mounted configuration files to make images portable and configurable.
- **Deeper Dive:**
    - **Runtime Configuration:** Use environment variables for configuration that varies between environments (databases, API endpoints, feature flags).
    - **Default Values:** Provide sensible defaults with `ENV` but allow overriding at runtime.
    - **Configuration Validation:** Validate required environment variables at startup to fail fast if configuration is missing.
    - **Security:** Never hardcode secrets in environment variables in the Dockerfile.
- **Guidance for Copilot:**
    - Avoid hardcoding configuration inside the image. Use `ENV` for default values, but allow overriding at runtime.
    - Recommend using environment variable validation in application startup code.
    - Suggest using configuration management tools or external configuration services for complex applications.
    - Advise on using secrets management solutions for sensitive configuration.
- **Example (Environment Variable Best Practices):**
```dockerfile
# Set default values
ENV NODE_ENV=production
ENV PORT=3000
ENV LOG_LEVEL=info

# Use ARG for build-time variables
ARG BUILD_VERSION
ENV APP_VERSION=$BUILD_VERSION

# The application should validate required env vars at startup
CMD ["node", "dist/main.js"]
```

### Container Security Best Practices

#### **1. Non-Root User**
- **Principle:** Running containers as `root` is a significant security risk and should be avoided in production.
- **Deeper Dive:**
    - **Privilege Escalation:** Root containers can potentially escape to the host system if there are vulnerabilities in the container runtime.
    - **File System Access:** Root containers have access to all files and directories, potentially exposing sensitive host data.
    - **Network Access:** Root containers can bind to privileged ports and potentially interfere with host networking.
    - **Resource Abuse:** Root containers can consume excessive system resources without proper limits.
- **Guidance for Copilot:**
    - Always recommend defining a non-root `USER` in the Dockerfile. Create a dedicated user for your application.
    - Ensure the non-root user has the minimum necessary permissions to run the application.
    - Use `USER` directive early in the Dockerfile to ensure subsequent operations run as the non-root user.
    - Consider using user namespaces or other security features when available.
- **Example (Secure User Creation):**
```dockerfile
# Create a dedicated user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set proper ownership of application files
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Ensure the user can write to necessary directories
VOLUME ["/app/data"]
```

#### **2. Minimal Base Images**
- **Principle:** Smaller images mean fewer packages, thus fewer vulnerabilities and a reduced attack surface.
- **Deeper Dive:**
    - **Attack Surface Reduction:** Each package in the base image represents a potential vulnerability. Fewer packages mean fewer potential attack vectors.
    - **Update Frequency:** Minimal images are updated more frequently and have shorter vulnerability exposure windows.
    - **Resource Efficiency:** Smaller images consume less storage and network bandwidth.
    - **Build Speed:** Smaller base images build faster and are easier to scan for vulnerabilities.
- **Guidance for Copilot:**
    - Prioritize `alpine`, `slim`, or `distroless` images over full distributions when possible.
    - Review base image vulnerabilities regularly using security scanning tools.
    - Consider using language-specific minimal images (e.g., `openjdk:17-jre-slim` instead of `openjdk:17`).
    - Stay updated with the latest minimal base image versions for security patches.
- **Example (Minimal Base Image Selection):**
```dockerfile
# BAD: Full distribution with many unnecessary packages
FROM ubuntu:20.04

# GOOD: Minimal Alpine-based image
FROM node:18-alpine

# BETTER: Distroless image for maximum security
FROM gcr.io/distroless/nodejs18-debian11
```

#### **3. Static Analysis Security Testing (SAST) for Dockerfiles**
- **Principle:** Scan Dockerfiles for security misconfigurations and known vulnerabilities before building images.
- **Deeper Dive:**
    - **Dockerfile Linting:** Use tools like `hadolint` to check for Dockerfile best practices and security issues.
    - **Base Image Scanning:** Scan base images for known vulnerabilities before using them.
    - **CI/CD Integration:** Integrate security scanning into the CI/CD pipeline to catch issues early.
    - **Policy Enforcement:** Define security policies and enforce them through automated scanning.
- **Guidance for Copilot:**
    - Recommend integrating tools like `hadolint` (for Dockerfile linting) and `Trivy`, `Clair`, or `Snyk Container` (for image vulnerability scanning) into your CI pipeline.
    - Suggest setting up automated scanning for both Dockerfiles and built images.
    - Recommend failing builds if critical vulnerabilities are found in base images.
    - Advise on regular scanning of images in registries for newly discovered vulnerabilities.
- **Example (Security Scanning in CI):**
```yaml
# GitHub Actions example
- name: Run Hadolint
  run: |
    docker run --rm -i hadolint/hadolint < Dockerfile

- name: Scan image for vulnerabilities
  run: |
    docker build -t myapp .
    trivy image myapp
```

#### **4. Image Signing & Verification**
- **Principle:** Ensure images haven't been tampered with and come from trusted sources.
- **Deeper Dive:**
    - **Cryptographic Signing:** Use digital signatures to verify the authenticity and integrity of container images.
    - **Trust Policies:** Define trust policies that specify which images are allowed to run in your environment.
    - **Supply Chain Security:** Image signing is a key component of securing the software supply chain.
    - **Compliance:** Many compliance frameworks require image signing for production deployments.
- **Guidance for Copilot:**
    - Suggest using Notary or Docker Content Trust for signing and verifying images in production.
    - Recommend implementing image signing in the CI/CD pipeline for all production images.
    - Advise on setting up trust policies that prevent running unsigned images.
    - Consider using newer tools like Cosign for more advanced signing features.
- **Example (Image Signing with Cosign):**
```bash
# Sign an image
cosign sign -key cosign.key myregistry.com/myapp:v1.0.0

# Verify an image
cosign verify -key cosign.pub myregistry.com/myapp:v1.0.0
```

#### **5. Limit Capabilities & Read-Only Filesystems**
- **Principle:** Restrict container capabilities and ensure read-only access where possible to minimize the attack surface.
- **Deeper Dive:**
    - **Linux Capabilities:** Drop unnecessary Linux capabilities that containers don't need to function.
    - **Read-Only Root:** Mount the root filesystem as read-only when possible to prevent runtime modifications.
    - **Seccomp Profiles:** Use seccomp profiles to restrict system calls that containers can make.
    - **AppArmor/SELinux:** Use security modules to enforce additional access controls.
- **Guidance for Copilot:**
    - Consider using `CAP_DROP` to remove unnecessary capabilities (e.g., `NET_RAW`, `SYS_ADMIN`).
    - Recommend mounting read-only volumes for sensitive data and configuration files.
    - Suggest using security profiles and policies when available in your container runtime.
    - Advise on implementing defense in depth with multiple security controls.
- **Example (Capability Restrictions):**
```dockerfile
# Drop unnecessary capabilities
RUN setcap -r /usr/bin/node

# Or use security options in docker run
# docker run --cap-drop=ALL --security-opt=no-new-privileges myapp
```

#### **6. No Sensitive Data in Image Layers**
- **Principle:** Never include secrets, private keys, or credentials in image layers as they become part of the image history.
- **Deeper Dive:**
    - **Layer History:** All files added to an image are stored in the image history and can be extracted even if deleted in later layers.
    - **Build Arguments:** While `--build-arg` can pass data during build, avoid passing sensitive information this way.
    - **Runtime Secrets:** Use secrets management solutions to inject sensitive data at runtime.
    - **Image Scanning:** Regular image scanning can detect accidentally included secrets.
- **Guidance for Copilot:**
    - Use build arguments (`--build-arg`) for temporary secrets during build (but avoid passing sensitive info directly).
    - Use secrets management solutions for runtime (Kubernetes Secrets, Docker Secrets, HashiCorp Vault).
    - Recommend scanning images for accidentally included secrets.
    - Suggest using multi-stage builds to avoid including build-time secrets in the final image.
- **Anti-pattern:** `ADD secrets.txt /app/secrets.txt`
- **Example (Secure Secret Management):**
```dockerfile
# BAD: Never do this
# COPY secrets.txt /app/secrets.txt

# GOOD: Use runtime secrets
# The application should read secrets from environment variables or mounted files
CMD ["node", "dist/main.js"]
```

#### **7. Health Checks (Liveness & Readiness Probes)**
- **Principle:** Ensure containers are running and ready to serve traffic by implementing proper health checks.
- **Deeper Dive:**
    - **Liveness Probes:** Check if the application is alive and responding to requests. Restart the container if it fails.
    - **Readiness Probes:** Check if the application is ready to receive traffic. Remove from load balancer if it fails.
    - **Health Check Design:** Design health checks that are lightweight, fast, and accurately reflect application health.
    - **Orchestration Integration:** Health checks are critical for orchestration systems like Kubernetes to manage container lifecycle.
- **Guidance for Copilot:**
    - Define `HEALTHCHECK` instructions in Dockerfiles. These are critical for orchestration systems like Kubernetes.
    - Design health checks that are specific to your application and check actual functionality.
    - Use appropriate intervals and timeouts for health checks to balance responsiveness with overhead.
    - Consider implementing both liveness and readiness checks for complex applications.
- **Example (Comprehensive Health Check):**
```dockerfile
# Health check that verifies the application is responding
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8080/health || exit 1

# Alternative: Use application-specific health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1
```

### Container Runtime & Orchestration Best Practices

#### **1. Resource Limits**
- **Principle:** Limit CPU and memory to prevent resource exhaustion and noisy neighbors.
- **Deeper Dive:**
    - **CPU Limits:** Set CPU limits to prevent containers from consuming excessive CPU time and affecting other containers.
    - **Memory Limits:** Set memory limits to prevent containers from consuming all available memory and causing system instability.
    - **Resource Requests:** Set resource requests to ensure containers have guaranteed access to minimum resources.
    - **Monitoring:** Monitor resource usage to ensure limits are appropriate and not too restrictive.
- **Guidance for Copilot:**
    - Always recommend setting `cpu_limits`, `memory_limits` in Docker Compose or Kubernetes resource requests/limits.
    - Suggest monitoring resource usage to tune limits appropriately.
    - Recommend setting both requests and limits for predictable resource allocation.
    - Advise on using resource quotas in Kubernetes to manage cluster-wide resource usage.
- **Example (Docker Compose Resource Limits):**
```yaml
services:
  app:
    image: myapp:<release-tag>
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

#### **2. Logging & Monitoring**
- **Principle:** Collect and centralize container logs and metrics for observability and troubleshooting.
- **Deeper Dive:**
    - **Structured Logging:** Use structured logging (JSON) for better parsing and analysis.
    - **Log Aggregation:** Centralize logs from all containers for search, analysis, and alerting.
    - **Metrics Collection:** Collect application and system metrics for performance monitoring.
    - **Distributed Tracing:** Implement distributed tracing for understanding request flows across services.
- **Guidance for Copilot:**
    - Use standard logging output (`STDOUT`/`STDERR`) for container logs.
    - Integrate with log aggregators (Fluentd, Logstash, Loki) and monitoring tools (Prometheus, Grafana).
    - Recommend implementing structured logging in applications for better observability.
    - Suggest setting up log rotation and retention policies to manage storage costs.
- **Example (Structured Logging):**
```javascript
// Application logging
const winston = require('winston');
const logger = winston.createLogger({
  format: winston.format.json(),
  transports: [new winston.transports.Console()]
});
```

#### **3. Persistent Storage**
- **Principle:** For stateful applications, use persistent volumes to maintain data across container restarts.
- **Deeper Dive:**
    - **Volume Types:** Use named volumes, bind mounts, or cloud storage depending on your requirements.
    - **Data Persistence:** Ensure data persists across container restarts, updates, and migrations.
    - **Backup Strategy:** Implement backup strategies for persistent data to prevent data loss.
    - **Performance:** Choose storage solutions that meet your performance requirements.
- **Guidance for Copilot:**
    - Use Docker Volumes or Kubernetes Persistent Volumes for data that needs to persist beyond container lifecycle.
    - Never store persistent data inside the container's writable layer.
    - Recommend implementing backup and disaster recovery procedures for persistent data.
    - Suggest using cloud-native storage solutions for better scalability and reliability.
- **Example (Docker Volume Usage):**
```yaml
services:
  database:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password

volumes:
  postgres_data:
```

#### **4. Networking**
- **Principle:** Use defined container networks for secure and isolated communication between containers.
- **Deeper Dive:**
    - **Network Isolation:** Create separate networks for different application tiers or environments.
    - **Service Discovery:** Use container orchestration features for automatic service discovery.
    - **Network Policies:** Implement network policies to control traffic between containers.
    - **Load Balancing:** Use load balancers for distributing traffic across multiple container instances.
- **Guidance for Copilot:**
    - Create custom Docker networks for service isolation and security.
    - Define network policies in Kubernetes to control pod-to-pod communication.
    - Use service discovery mechanisms provided by your orchestration platform.
    - Implement proper network segmentation for multi-tier applications.
- **Example (Docker Network Configuration):**
```yaml
services:
  web:
    image: nginx
    networks:
      - frontend
      - backend

  api:
    image: myapi
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true
```

#### **5. Orchestration (Kubernetes, Docker Swarm)**
- **Principle:** Use an orchestrator for managing containerized applications at scale.
- **Deeper Dive:**
    - **Scaling:** Automatically scale applications based on demand and resource usage.
    - **Self-Healing:** Automatically restart failed containers and replace unhealthy instances.
    - **Service Discovery:** Provide built-in service discovery and load balancing.
    - **Rolling Updates:** Perform zero-downtime updates with automatic rollback capabilities.
- **Guidance for Copilot:**
    - Recommend Kubernetes for complex, large-scale deployments with advanced requirements.
    - Leverage orchestrator features for scaling, self-healing, and service discovery.
    - Use rolling update strategies for zero-downtime deployments.
    - Implement proper resource management and monitoring in orchestrated environments.
- **Example (Kubernetes Deployment):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:<release-tag>
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Dockerfile Review Checklist

- [ ] Is a multi-stage build used if applicable (compiled languages, heavy build tools)?
- [ ] Is a minimal, specific base image used (e.g., `alpine`, `slim`, versioned)?
- [ ] Are layers optimized (combining `RUN` commands, cleanup in same layer)?
- [ ] Is a `.dockerignore` file present and comprehensive?
- [ ] Are `COPY` instructions specific and minimal?
- [ ] Is a non-root `USER` defined for the running application?
- [ ] Is the `EXPOSE` instruction used for documentation?
- [ ] Is `CMD` and/or `ENTRYPOINT` used correctly?
- [ ] Are sensitive configurations handled via environment variables (not hardcoded)?
- [ ] Is a `HEALTHCHECK` instruction defined?
- [ ] Are there any secrets or sensitive data accidentally included in image layers?
- [ ] Are there static analysis tools (Hadolint, Trivy) integrated into CI?

### Troubleshooting Docker Builds & Runtime

#### **1. Large Image Size**
- Review layers for unnecessary files. Use `docker history <image>`.
- Implement multi-stage builds.
- Use a smaller base image.
- Optimize `RUN` commands and clean up temporary files.

#### **2. Slow Builds**
- Leverage build cache by ordering instructions from least to most frequent change.
- Use `.dockerignore` to exclude irrelevant files.
- Use `docker build --no-cache` for troubleshooting cache issues.

#### **3. Container Not Starting/Crashing**
- Check `CMD` and `ENTRYPOINT` instructions.
- Review container logs (`docker logs <container_id>`).
- Ensure all dependencies are present in the final image.
- Check resource limits.

#### **4. Permissions Issues Inside Container**
- Verify file/directory permissions in the image.
- Ensure the `USER` has necessary permissions for operations.
- Check mounted volumes permissions.

#### **5. Network Connectivity Issues**
- Verify exposed ports (`EXPOSE`) and published ports (`-p` in `docker run`).
- Check container network configuration.
- Review firewall rules.

### Conclusion

Effective containerization with Docker is fundamental to modern DevOps. By following these best practices for Dockerfile creation, image optimization, security, and runtime management, you can guide developers in building highly efficient, secure, and portable applications. Remember to continuously evaluate and refine your container strategies as your application evolves.

---

<!-- End of Containerization & Docker Best Practices Instructions -->

## Dev Container Configuration

<!-- source: github/awesome-copilot instructions/devcontainers.instructions.md -->

Twelve rules for reviewing and writing `devcontainer.json`, Dev Container Features, and the lifecycle configuration that GitHub Codespaces and the reference CLI act on. Each rule states the assertion, what to look for, and the concrete change, and links the source it comes from so the claim can be checked rather than trusted.

Every rule here is a reading task. Some need only `devcontainer.json`; some also read a Feature's `devcontainer-feature.json` or its `install.sh`; and some read what else the repository holds — a Codespaces prebuild or CI configuration, a Dockerfile step, an ownership-correcting script. None requires building an image, starting a container, or having the `devcontainer` CLI installed — which is what makes them usable in a code review, where no command can be run at all.

Two rules are easy to over-apply. Read the paragraphs marked **Do not report** before flagging anything about secrets in `remoteEnv` or about `updateRemoteUserUID`.

### What the file tells you, and what it does not

At runtime, `devcontainer.json` is merged with the `devcontainer.metadata` label baked into the image, and the specification's image-metadata section states: "When the order matters, the devcontainer.json is considered last."

So a value **present** in the file wins that merge and can be relied on. A value **absent** from the file may still be supplied by the image label, and the file alone cannot tell you it was not. Say what the file states, and say where the label could still change it. Do not report the absence of a lifecycle command, `waitFor`, `remoteEnv`, `containerEnv`, `mounts`, `remoteUser`, `containerUser`, `updateRemoteUserUID` or `userEnvProbe` as proof that the behaviour is absent.

**Where a property is exempt from that caution, read it off a positive marker — never infer it from absence.** The property reference tags each storable property: "Metadata properties marked with a 🏷️ can be stored in the `devcontainer.metadata` **container image label** in addition to `devcontainer.json`." An *untagged row* attests that a property is not label-storable. A property with **no row at all** is one the source is silent about, and silence is not immunity. Do not subtract one list from another to obtain immunity: the image-metadata document declares its own enumerations open — "We can add to these lists as we add more properties to the dev container configuration and the feature metadata." — and the complement of an open list is not a fact.

Read that way, of the properties the rules below reason about, `features`, `overrideFeatureInstallOrder` and `appPort` have untagged rows and are attested not label-storable. Top-level `extensions`, `settings` and `devPort` are VS Code schema properties with no row in the reference at all: unattested in either direction, so do not call them label-immune.

That costs the deprecated-properties rule below nothing, because what protects it is not immunity but **direction**. It reports only keys it can *see* in the configuration, and a value present in the file wins the merge — so the three unattested names can cost it a missed finding and can never produce a false one. That makes the finding sound; it does not make the rule label-immune, and the two are not the same thing. Apply the same test to every rule here: report what the file states, and say where the label could still change it.

Sources: <https://containers.dev/implementors/spec/>, <https://containers.dev/implementors/json_reference/> and <https://github.com/devcontainers/spec/blob/main/docs/specs/image-metadata.md>

### Lifecycle commands

#### Cacheable setup belongs in `onCreateCommand` or `updateContentCommand`, never in `postCreateCommand`

A Codespaces prebuild performs "setup operations up to and including any `onCreateCommand` and `updateContentCommand` commands in the `devcontainer.json` file. No `postCreateCommand` commands are run during the creation of a prebuild." The reference CLI's `--prebuild` flag behaves the same way: it stops after `updateContentCommand` and re-runs it. Dependency installation left in `postCreateCommand` is therefore never baked into the prebuild and is paid again on every codespace start.

Look for expensive, cacheable work in `postCreateCommand` — `npm ci`, `npm install`, `yarn install`, `pnpm install`, `pip install`, `poetry install`, `bundle install`, `go mod download`, `cargo fetch`, `apt-get install`, `make`, `gradle`, `mvn` — while `onCreateCommand` and `updateContentCommand` are absent or trivial. Check the object form entry by entry, not just the string form.

**Fix:** move the cacheable half into `onCreateCommand`, which the reference describes as used by cloud services "when caching or prebuilding a container. This means that it will not typically have access to user-scoped assets or secrets", or into `updateContentCommand`, which those services "will also periodically execute ... to refresh cached or prebuilt containers". Leave in `postCreateCommand` only work that needs the assigned user's own credentials or permissions.

**Scope.** This only costs a project that actually uses prebuilds — a Codespaces prebuild configuration, or a CI job invoking `devcontainer up --prebuild`. A repository that never prebuilds is not wrong to install dependencies in `postCreateCommand`. Say so rather than reporting a defect.

Sources: <https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds> and <https://containers.dev/implementors/json_reference/>

#### `waitFor` accepts exactly five values, and `postAttachCommand` is not one of them

The base schema fixes the enum: `"enum": [ "initializeCommand", "onCreateCommand", "updateContentCommand", "postCreateCommand", "postStartCommand" ]`, described as "The user command to wait for before continuing execution in the background while the UI is starting up. The default is \"updateContentCommand\"."

Anything outside those five strings is invalid. `postAttachCommand` is the value people reach for, because it is a real lifecycle hook and the only one missing from the enum. Nothing in a normal workflow catches the mistake: the reference CLI parses and merges the configuration but does not validate it against the JSON Schema, so an invalid `waitFor` reaches the tool unchallenged, and schema registration only produces editor-time squiggles. (That last mechanism is stated by no document; it is checkable by inspection — treat it as background, not as cited.)

**Fix:** choose from the five. If the intent was "block until my setup finishes", the value is `postCreateCommand`, not `postAttachCommand`. If the intent was the default, delete the property. Note what the default implies: `postCreateCommand` runs in the background after the tool reports success, so a slow `postCreateCommand` is not a hang.

Source: <https://github.com/devcontainers/spec/blob/main/schemas/devContainer.base.schema.json>

#### Lifecycle hooks take a string, an array, or an object — and object entries run in parallel

The specification extends every lifecycle script to the object form: "The key of the `object` will be a unique name for the command and the value will be the `string` or `array` command. ... Each entry in the `object` will be run in parallel during that lifecycle step."

Determine which of the three forms each hook uses before applying any other lifecycle rule. A string runs through `/bin/sh`, so `&&` chains. An array is executed directly with no shell, so `["npm start && npm test"]` is one argv and `&&` is a literal argument, not an operator. An object runs every entry concurrently: flag entries that assume ordering between each other, such as one entry creating a directory or database that another entry writes to. The same source adds that "Each command must exit successfully for the stage to be considered successful", so one failing parallel entry fails the whole stage.

**Fix:** use the object form only for genuinely independent work. Where entries must be sequenced, put them in one string joined with `&&`, or in one script invoked from the hook. Use the array form deliberately when an argument must survive verbatim without shell parsing — not by accident.

Source: <https://github.com/devcontainers/spec/blob/main/docs/specs/parallel-lifecycle-script-execution.md>

### Secrets and environment

#### `remoteEnv` is written into the image metadata label by default, so literal credentials there are readable by anyone who can pull the image

The reference CLI defines a hidden flag: `'omit-config-remote-env-from-metadata': { type: 'boolean', default: false, hidden: true, description: 'Omit remoteEnv from devcontainer.json for container metadata label' }`.

`default: false` on the *omit* flag is the CLI stating outright that the omission is off — `remoteEnv` **is** written to the `devcontainer.metadata` label unless you ask otherwise. `hidden: true` sharpens it: the flag does not appear in `--help`, so an operator will not discover the behaviour by asking the tool.

**The value decides, not the key. Do not report** an entry whose value is a substitution reference — `${localEnv:NAME}` or `${containerEnv:NAME}`, with or without a `:default` — at any severity, whatever the key is called. The literal never enters the file and never reaches the image label, which is this rule's entire subject. `"GITHUB_TOKEN": "${localEnv:GITHUB_TOKEN}"` is precisely the form the fix below prescribes; flagging it contradicts the rule's own remedy. A secret-shaped key name — `TOKEN`, `SECRET`, `KEY`, `PASSWORD`, `PASSWD`, `CREDENTIAL`, `_PAT` — is a reason to read the value and is never by itself a reason to report.

Report a literal that looks like a credential: a long opaque string, a recognisable prefix such as `sk_`, `ghp_`, `github_pat_`, `AKIA`, `xoxb-`, `glpat-`, a PEM header, or a connection string with an embedded password. Do not report a literal that is plainly not a credential — an environment name, a port, a path, a host, or a URL carrying no credential. Where a literal is genuinely ambiguous, let the key name decide the direction: under a secret-shaped key, report it, since a short low-entropy value such as `hunter2` under `PASSWORD` is still a finding unless it is an obvious placeholder like `changeme` or `<your-key-here>`; under any other key, describe what you see rather than asserting a leak.

`containerEnv` is worse than `remoteEnv` for a literal, because it becomes a Dockerfile `ENV` and is baked into a layer. Apply the same value test — never a key-name test — to `build.args`, which are visible in image history.

**Fix:** declare the name under the top-level `secrets` property so the configuration documents what is needed — that property is declarative only, it injects nothing — and pass the value at run time with `--secrets-file <json>` on `up` or `run-user-commands`. If a value must stay in `remoteEnv`, indirect it through `${localEnv:NAME}` so the literal is not committed, and remember the label still records the reference. **Keep the secrets file out of the repository:** a path inside the workspace is one `git add .` away from committing the secret this rule exists to protect. Put it under the user's home directory, or, if it must live in the tree, add it to `.gitignore` in the same change and verify with `git check-ignore`.

Source: <https://github.com/devcontainers/cli/blob/main/src/spec-node/devContainersSpecCLI.ts>

#### `userEnvProbe` decides which shell startup files the lifecycle environment sees

The property "Indicates the type of shell to use to \"probe\" for user environment variables to include in `devcontainer.json` supporting services' / tools' processes: `none`, `interactiveShell`, `loginShell`, or `loginInteractiveShell` (default)."

`"none"` is the high-signal value: no startup file is read at all, so anything a Feature or Dockerfile put on `PATH` via `~/.bashrc` or `/etc/profile.d` is invisible to lifecycle commands even though an interactive terminal in the same container finds it. `"loginShell"` and `"interactiveShell"` each read only half the files — the same page notes that "bash interactive shells will typically include variables set in `/etc/bash.bashrc` and `~/.bashrc` while login shells usually include variables from `/etc/profile` and `~/.profile`. Setting this property to `loginInteractiveShell` will get variables from all four files." Suspect this rule whenever a lifecycle command fails with "command not found" for a tool that is demonstrably installed.

**Fix:** prefer the default `loginInteractiveShell` and delete an explicit `userEnvProbe` unless something depends on narrowing it. Where the environment must not depend on shell startup files at all, set the variables in `containerEnv` (visible to every process in the container) or `remoteEnv` (tool processes only — see the secrets rule above before putting anything sensitive there), or invoke the tool by absolute path in the lifecycle command.

Source: <https://containers.dev/implementors/json_reference/>

### Dev Container Features

#### `overrideFeatureInstallOrder` cannot reorder a dependency edge

The Features specification is explicit: the property "must not influence the dependency relationship as defined by the dependency graph ... and shall only be evaulated at the round-based sorting step ... this property cannot \"pull forward\" a Feature until all of its dependencies (both soft and hard) have been installed."

Read `overrideFeatureInstallOrder` against the `dependsOn` and `installsAfter` edges of the Features listed in `features`. Flag an entry that tries to place a Feature before something it depends on: the requested order will silently not happen. The mechanism, from the same page, is that the property assigns a `roundPriority` "to all nodes that match the Feature identifier (version omitted) present in the property" — priority reorders only *within* a round and never moves a node into an earlier round. Also flag an identifier listed there that is not among the Features being installed; the same page says the tool "may fail the dependency resolution step" for that.

**Fix:** if the ordering is a real requirement, express it in the Feature's own `dependsOn` (hard, recursive, can carry options and a pinned version) or `installsAfter` (soft, non-recursive, dropped if the named Feature is not otherwise installed). Use `overrideFeatureInstallOrder` only to break ties the graph leaves open.

Source: <https://containers.dev/implementors/features/>

#### Feature dependency resolution happens once, at creation from `devcontainer.json` — and Features must be idempotent

From the dependency specification: "For subsequent creations from an image (or resumes of a dev container), the dependency tree is **not** re-calculated. ... Since two Features with different options are considered different, a single Feature may be installed more than once. Features should be idempotent."

Two symptoms. First, a configuration that starts `FROM` a previously built dev container image and expects a Feature version bump or a changed `dependsOn` to take effect: it will not, because the *resolved* Feature set is frozen onto the `devcontainer.metadata` label at first creation. Second, the same Feature referenced twice with different options — directly in `features`, or once directly and once pulled in by another Feature's `dependsOn` — which installs it twice. If you author Features, read `install.sh` for non-idempotent steps: appending to `PATH`, `~/.bashrc` or `/etc/profile.d` without a guard, `useradd` without a check, unconditional `git clone`.

**Fix:** to pick up changed dependencies, recreate from `devcontainer.json` rather than rebuilding from the image — the source states the image or dev container must be deleted and recreated. In an authored Feature, make every step re-runnable: guard appends with a marker grep, use `install -D`, check before creating users, and make downloads overwrite rather than append.

Source: <https://github.com/devcontainers/spec/blob/main/docs/specs/feature-dependencies.md>

#### A Feature's `install.sh` runs as root, so read the eventual user from `_REMOTE_USER` rather than hardcoding one

"The `install.sh` script for each Feature should be executed as `root` during a container image build. ... `_REMOTE_USER` and `_CONTAINER_USER` environment variables are passed to the Features scripts with `_CONTAINER_USER` being the container's user". The home directories have their own variables: "the home folders of the two users are passed to the Feature scripts as `_REMOTE_USER_HOME` and `_CONTAINER_USER_HOME` environment variables."

In an authored `install.sh`, flag a hardcoded `vscode`, `node`, `codespace` or `root` username, and flag any write into a home directory computed as `/home/$USER` or `~`. When consuming Features, the visible symptom is files under the workspace or home directory owned by `root` that the `remoteUser` cannot write.

**Fix:** read the user from `_REMOTE_USER`, falling back to `_CONTAINER_USER` (the specification says the two are equal when no `remoteUser` is configured), and the home directory from `_REMOTE_USER_HOME`. Drop privileges for user-scoped work with `su "$_REMOTE_USER" -c '...'`, or `chown -R "$_REMOTE_USER" "$_REMOTE_USER_HOME/<path>"` after writing as root. Never assume `sudo` exists in the base image.

Source: <https://containers.dev/implementors/features/>

### Users, ownership and UIDs

#### A named volume mounted to dodge the bind-mount penalty comes up root-owned and needs an explicit `chown`

The performance guidance is direct: "add a `postCreateCommand` to update the owner of the folder you mount since it may have been mounted as root".

Look for a `mounts` entry with `type=volume` — typically `source=${localWorkspaceFolderBasename}-node_modules,target=${containerWorkspaceFolder}/node_modules,type=volume` — or a `workspaceMount` with `type=volume`, in a configuration that also sets a non-root `remoteUser` or `containerUser`. Flag it when no `postCreateCommand` chowns that target. The failure is a permission error on first write into the mounted directory, not a build failure, so it surfaces late. The same page notes the step "is not required if you will be running in the container as `root`" — a root container is not a finding here.

**Fix:** add the ownership fix to `postCreateCommand`, naming the same user as `remoteUser`, for example `"postCreateCommand": "sudo chown node node_modules"`. If the whole tree is on a volume, `workspaceMount` and `workspaceFolder` must both be set — the reference says of each that it "Requires `workspaceFolder` be set as well" and "Requires `workspaceMount` be set". Note that a `mounts`-based optimisation is local-only: Codespaces ignores bind mounts other than the Docker socket, so verify the configuration still works there. (That Codespaces limitation is stated by no document cited here; treat it as checkable background, not as cited.)

Source: <https://code.visualstudio.com/remote/advancedcontainers/improve-performance>

#### `updateRemoteUserUID` defaults to true on Linux — and an absent property is not a defect

The reference states: "On Linux, if `containerUser` or `remoteUser` is specified, the user's UID/GID will be updated to match the local user's UID/GID to avoid permission problems with bind mounts. Defaults to `true`."

**Do not report an absent `updateRemoteUserUID`.** It defaults to true, and on a Linux workstation that default is exactly what keeps bind-mounted files writable. A configuration that sets `remoteUser` or `containerUser` and leaves `updateRemoteUserUID` unset is the ordinary, correct case: emit nothing for it.

The default costs something in only two situations, and one of them must be visible in the repository before there is anything to report.

1. **The pipeline names an image the build does not produce.** With the default in effect on Linux, the reference CLI derives a second, `-uid`-suffixed image (visible in the CLI source at `src/spec-node/containerFeatures.ts`; stated by no document, so treat it as verified by inspection rather than cited), so a workflow that pins, tags, publishes or scans a specific `--image-name` is not operating on the image that actually runs. Report only on evidence of such a workflow: a CI invocation passing `--image-name`, a `devcontainers/ci` step setting `imageName` or `push`, or a documented prebuilt image tag.
2. **A Linux-only ownership problem is being masked.** The step does not apply on macOS or Windows hosts, so an ownership workaround that makes permissions look right on a Mac may hide behaviour that differs on Linux. Report only when such a workaround is actually present. The forms below are examples, not an exhaustive list — read for the intent, which is a step that exists to correct file ownership or permissions: a `chown` or `chmod`, a `sudo` ownership step, an `install -o`, a `setfacl`, or a script whose name says as much. A step that merely works *around* an ownership mismatch without changing ownership — `git config --global --add safe.directory`, for instance — is not this symptom and is not a finding.

If neither symptom is present, this rule is informational: it explains a default, and a default being in effect is not a finding.

**Fix:** in CI, where the host UID is irrelevant and the extra build is pure cost, turn it off. The `devcontainers/ci` action exposes `skipContainerUserIdUpdate`, documented as "For non-root Dev Containers (i.e. where `remoteUser` is specified), the action attempts to make the container user UID and GID match those of the host user. Set this to true to skip this step". The CLI equivalent is `--update-remote-user-uid-default never`. Locally on Linux, leave it on. Set `"updateRemoteUserUID": false` in the configuration only when the container UID must stay fixed everywhere.

Sources: <https://containers.dev/implementors/json_reference/> and <https://github.com/devcontainers/ci>

### Deprecated properties

#### Top-level `extensions`, `settings` and `devPort` belong under `customizations.vscode`, and `appPort` is superseded by `forwardPorts`

The VS Code schema marks the top-level properties: `"deprecated": true, "deprecationMessage": "Use 'customizations/vscode/extensions' instead"`, with the identical shape for `settings` and `devPort`.

That pair sits on the **top-level** property. The schema also defines `customizations.vscode.extensions`, which opens identically but carries no deprecation — searching the schema for `"extensions"` finds the wrong one first, so match on the `deprecated` pair rather than the property name. Separately, flag `appPort`; the reference says of it: "In most cases, we recommend using the new \[forwardPorts property\](#general-devcontainerjson-properties). This property accepts a port or array of ports that should be published locally when the container is running." These are deprecations, not breakage — the old keys still work — so report them as modernisation.

**Fix:** move `extensions` and `settings` under `customizations.vscode` verbatim, and `devPort` to `customizations.vscode.devPort`. The same namespace now also holds `mcp`, described in that schema as "Model Context Protocol server configurations" — put Model Context Protocol server configuration there rather than inventing a top-level key. Replace `appPort` with `forwardPorts` unless the port must be *published* on all interfaces rather than forwarded, in which case keep `appPort` and say why. Remember `customizations` is an open namespace: the specification only says each tool "should use a JSON object subproperty with a unique name", so an unknown key under it is not necessarily wrong.

Sources: <https://github.com/microsoft/vscode/blob/main/extensions/configuration-editing/schemas/devContainer.vscode.schema.json> and <https://containers.dev/implementors/json_reference/>

### Vendor-specific: running Claude Code in a dev container

**This rule is not part of the Dev Container specification.** Every mechanical claim below is stated in Anthropic's own documentation, but nothing in the specification requires any of it, and a dev container that never runs Claude Code is not defective for lacking it. Apply this rule only to a configuration that installs or runs Claude Code, and never present it as specification.

The vendor documentation states: "Because the container runs Claude Code as a non-root user and confines command execution to the container, you can pass `--dangerously-skip-permissions` for unattended operation. The CLI rejects this flag when launched as root, so confirm `remoteUser` is set to a non-root account."

Then check three things. First, `remoteUser` is set and is not `root`. Second, there is a `mounts` entry for `~/.claude` **and** a `containerEnv` entry for `CLAUDE_CONFIG_DIR` pointing at the same path — the same page states that "mounting a volume at `~/.claude` alone doesn't keep you signed in", because the OAuth account file sits outside that directory, and a volume with no matching environment variable is the common half-configuration. Third, if the configuration runs the reference egress firewall, that page states it "adds the `NET_ADMIN` and `NET_RAW` capabilities through `runArgs`" — a firewall script without those capabilities fails at start.

**Fix:** set a non-root `remoteUser` and add both halves of the auth mount, substituting the real home directory of that user:

```json
{
  "remoteUser": "node",
  "mounts": ["source=claude-code-config-${devcontainerId},target=/home/node/.claude,type=volume"],
  "containerEnv": { "CLAUDE_CONFIG_DIR": "/home/node/.claude" }
}
```

`${devcontainerId}` in the volume name isolates state per project; drop it to share one login across repositories. If `containerEnv` already exists, add the key to it rather than adding a second object. For the firewall, add `"runArgs": ["--cap-add=NET_ADMIN", "--cap-add=NET_RAW"]`. Treat the `anthropics/claude-code` reference configuration as a worked example rather than a maintained base image, and do not mount host secrets such as `~/.ssh` into the container.

Source: <https://code.claude.com/docs/en/devcontainer>

### Provenance and limits

Eleven of these twelve rules are stated by the Dev Container specification, the reference CLI source, or official vendor documentation, and apply to any dev container. The twelfth — the Claude Code rule — is vendor-documented but conditional on a tool the specification does not mention, which is why it is fenced off in its own section above. Three passages are flagged in place as verified by inspection rather than cited: the reference CLI's lack of JSON Schema validation, the Codespaces bind-mount limitation, and the derived `-uid` image name. Everything else quoted here was read at its linked source, and every link resolved, on 2026-09-01.

No false-positive rate has been measured for any of these rules, so none carries a severity label. The ordering above is editorial. Report what the configuration states and what the source says about it; do not attach a confidence number that nobody measured.
