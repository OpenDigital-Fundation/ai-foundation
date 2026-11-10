# Incident response — derived guides

Part of `platform:incident-response`.

## Connectivity Triage

<!-- source: wshobson/agents plugins/incident-response/skills/connectivity-triage/SKILL.md#fast-decision-flow -->

### Fast Decision Flow

Work from the symptom toward the narrowest discriminating check:

```text
symptom
  -> local link / LAN evidence
  -> DNS configuration and resolution
  -> destination reachability
  -> path quality
  -> application / service timing
  -> fault-domain assessment
```

Stop early when the evidence is already sufficient. Do not run every probe mechanically.

#### 1. Define the symptom

Record the affected application or process, destination hostname or URL, when the failure started, whether it is continuous or intermittent, and whether unrelated destinations still work.

If the symptom is application-specific, preserve the exact hostname or URL the application uses. Testing an unrelated public site can establish general connectivity but cannot prove the affected service is healthy.

#### 2. Check local-link / LAN evidence

When available, run a bounded `networkQuality` sample for a broad responsiveness and throughput signal. If `networkQuality` is unavailable, continue; it is optional.

If a known local gateway or same-LAN target is available, compare a short bounded `ping` sample to that local target with a short sample to the remote destination. Do not invent a gateway address. If no local target is known, leave the LAN segment unproven and continue.

Useful pattern:

```bash
ping -c 5 <known-local-target>
ping -c 5 <destination>
```

#### 3. Separate DNS configuration from DNS behavior

Inspect the system resolver state, especially when VPNs, split DNS, or scoped resolvers may be involved:

```bash
scutil --dns
```

Then test the destination name directly with a bounded DNS query:

```bash
dig +time=2 +tries=1 <hostname>
```

Treat these as different evidence. `scutil --dns` shows resolver configuration; `dig` shows query behavior. A successful lookup does not prove the returned endpoint is reachable.

#### 4. Test reachability and path quality

Use a short `ping` sample when ICMP is a useful signal:

```bash
ping -c 5 <destination>
```

If the hostname resolves, test the returned address separately only when doing so helps distinguish DNS behavior from path failure. If resolution currently fails, use an address only when it was previously observed from trustworthy incident evidence; otherwise leave address-level reachability unknown.

Use a bounded numeric traceroute when path visibility would reduce uncertainty:

```bash
traceroute -n -q 1 -m 20 <destination>
```

A silent or changing hop is an observation, not proof that the hop is broken. Routers may filter or rate-limit traceroute traffic while forwarding application traffic normally.

#### 5. Inspect the affected application's live network activity

When the problem is process-specific, use a bounded `nettop` capture rather than watching indefinitely:

```bash
nettop -n -L 3 -p <process-name-or-pid>
```

Use it to confirm whether the process is opening connections, which endpoints it is using, and whether traffic is flowing. Lack of visible activity may mean the application never attempted the connection; it does not by itself identify why.

#### 6. Time the application path

For HTTP(S), use curl phase timing against the actual affected endpoint when a safe read-only request is available. Confirm the incident-supplied endpoint is a complete `http://` or `https://` URL, preserve its original scheme, and pass the URL as one quoted argument rather than interpolating arbitrary incident text into the shell command:

```bash
curl -sS -o /dev/null \
  -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' \
  --connect-timeout 5 --max-time 15 '<affected-http-or-https-url>'
```

Interpret the phases comparatively. High time-to-first-byte can include server processing, so it is not proof of network latency.

## incident-responder

<!-- source: wshobson/agents plugins/incident-response/agents/incident-responder.md#post-incident-process,immediate-actions-first-5-minutes,sre-best-practices -->

### Immediate Actions (First 5 minutes)

#### 1. Assess Severity & Impact

- **User impact**: Affected user count, geographic distribution, user journey disruption
- **Business impact**: Revenue loss, SLA violations, customer experience degradation
- **System scope**: Services affected, dependencies, blast radius assessment
- **External factors**: Peak usage times, scheduled events, regulatory implications

#### 2. Establish Incident Command

- **Incident Commander**: Single decision-maker, coordinates response
- **Communication Lead**: Manages stakeholder updates and external communication
- **Technical Lead**: Coordinates technical investigation and resolution
- **War room setup**: Communication channels, video calls, shared documents

#### 3. Immediate Stabilization

- **Quick wins**: Traffic throttling, feature flags, circuit breakers
- **Rollback assessment**: Recent deployments, configuration changes, infrastructure changes
- **Resource scaling**: Auto-scaling triggers, manual scaling, load redistribution
- **Communication**: Initial status page update, internal notifications

### Post-Incident Process

#### Immediate Post-Incident (24 hours)

- **Service stability**: Continued monitoring, alerting adjustments
- **Communication**: Resolution announcement, customer updates
- **Data collection**: Metrics export, log retention, timeline documentation
- **Team debrief**: Initial lessons learned, emotional support

#### Blameless Post-Mortem

- **Timeline analysis**: Detailed incident timeline with contributing factors
- **Root cause analysis**: Five whys, fishbone diagrams, systems thinking
- **Contributing factors**: Human factors, process gaps, technical debt
- **Action items**: Prevention measures, detection improvements, response enhancements
- **Follow-up tracking**: Action item completion, effectiveness measurement

#### System Improvements

- **Monitoring enhancements**: New alerts, dashboard improvements, SLI adjustments
- **Automation opportunities**: Runbook automation, self-healing systems
- **Architecture improvements**: Resilience patterns, redundancy, graceful degradation
- **Process improvements**: Response procedures, communication templates, training
- **Knowledge sharing**: Incident learnings, updated documentation, team training

### SRE Best Practices

#### Error Budget Management

- **Burn rate analysis**: Current error budget consumption
- **Policy enforcement**: Feature freeze triggers, reliability focus
- **Trade-off decisions**: Reliability vs. velocity, resource allocation

#### Reliability Patterns

- **Circuit breakers**: Automatic failure detection and isolation
- **Bulkhead pattern**: Resource isolation to prevent cascading failures
- **Graceful degradation**: Core functionality preservation during failures
- **Retry policies**: Exponential backoff, jitter, circuit breaking

#### Continuous Improvement

- **Incident metrics**: MTTR, MTTD, incident frequency, user impact
- **Learning culture**: Blameless culture, psychological safety
- **Investment prioritization**: Reliability work, technical debt, tooling
- **Training programs**: Incident response, on-call best practices
