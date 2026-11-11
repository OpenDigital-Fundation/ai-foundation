# Compliance programs — derived guides

Part of `legal-compliance:compliance-programs`.

## Data Privacy Compliance

<!-- source: davila7/claude-code-templates cli-tool/components/skills/enterprise-communication/data-privacy-compliance/SKILL.md#data-subject-rights-implementation,privacy-by-design-principles,consent-management -->

### Data Subject Rights Implementation

#### 1. Right to Access (GDPR Art. 15 / CCPA § 1798.100)

**Request Handler:**
```javascript
async function handleAccessRequest(userId, email) {
  // Verify identity
  const verified = await verifyIdentity(email);
  if (!verified) throw new Error('Identity verification failed');

  // Collect all personal data
  const userData = await collectUserData(userId);

  // Format for readability
  const report = {
    personalInfo: userData.profile,
    activityLogs: userData.activities,
    preferences: userData.settings,
    thirdPartySharing: userData.dataSharing,
    retentionPeriod: '2 years from last activity',
    dataProtectionOfficer: 'dpo@company.com'
  };

  // Generate downloadable report
  const pdf = await generatePDFReport(report);

  // Log request for compliance
  await logAccessRequest(userId, 'completed');

  return pdf;
}
```

**Response Timeline:**
- GDPR: 1 month (extendable to 3 months)
- CCPA: 45 days (extendable to 90 days)

#### 2. Right to Deletion (GDPR Art. 17 / CCPA § 1798.105)

**Deletion Handler:**
```javascript
async function handleDeletionRequest(userId, email) {
  // Verify identity
  const verified = await verifyIdentity(email);
  if (!verified) throw new Error('Identity verification failed');

  // Check for legal obligations to retain
  const mustRetain = await checkRetentionRequirements(userId);
  if (mustRetain.required) {
    return {
      status: 'partial_deletion',
      retained: mustRetain.data,
      reason: mustRetain.legalBasis,
      retentionPeriod: mustRetain.period
    };
  }

  // Delete from all systems
  await Promise.all([
    deleteFromDatabase(userId),
    deleteFromBackups(userId), // Mark for deletion in next backup cycle
    deleteFromAnalytics(userId),
    deleteFromThirdPartyServices(userId),
    revokeAPIKeys(userId),
    anonymizeHistoricalRecords(userId)
  ]);

  // Confirm deletion
  await sendDeletionConfirmation(email);
  await logDeletionRequest(userId, 'completed');

  return { status: 'deleted', timestamp: new Date() };
}
```

**Exceptions (when deletion can be refused):**
- Legal obligations (tax records, contracts)
- Public interest/scientific research
- Defense of legal claims
- Exercise of freedom of expression

#### 3. Right to Data Portability (GDPR Art. 20)

**Export Handler:**
```javascript
async function handlePortabilityRequest(userId, format = 'json') {
  const userData = await collectUserData(userId);

  // Structure in machine-readable format
  const portableData = {
    exportDate: new Date().toISOString(),
    userId: userId,
    data: {
      profile: userData.profile,
      content: userData.userGeneratedContent,
      settings: userData.preferences,
      history: userData.activityHistory
    }
  };

  // Support multiple formats
  if (format === 'csv') {
    return convertToCSV(portableData);
  } else if (format === 'xml') {
    return convertToXML(portableData);
  }

  return portableData; // JSON by default
}
```

**Requirements:**
- Structured, commonly used, machine-readable format
- Ability to transmit directly to another controller
- Only applies to data provided by data subject
- Only for automated processing based on consent or contract

#### 4. Right to Object (GDPR Art. 21)

**Objection Handler:**
```javascript
async function handleObjectionRequest(userId, processingType) {
  switch (processingType) {
    case 'direct_marketing':
      // Must stop immediately
      await disableMarketing(userId);
      await updateConsent(userId, 'marketing', false);
      break;

    case 'legitimate_interest':
      // Assess if we have compelling grounds
      const assessment = await assessLegitimateInterest(userId);
      if (!assessment.compelling) {
        await stopProcessing(userId, processingType);
      }
      return assessment;

    case 'profiling':
      await disableProfiling(userId);
      await updateConsent(userId, 'profiling', false);
      break;

    default:
      throw new Error('Invalid processing type');
  }

  await logObjectionRequest(userId, processingType, 'granted');
}
```

### Consent Management

#### Consent Requirements (GDPR)

**Valid Consent Must Be:**
1. Freely given (no coercion)
2. Specific (for each purpose)
3. Informed (clear language)
4. Unambiguous (clear affirmative action)
5. Withdrawable (as easy to withdraw as to give)

**Consent Implementation:**
```html
<!-- Good: Granular consent -->
<form>
  <h3>Privacy Preferences</h3>

  <label>
    <input type="checkbox" name="essential" checked disabled>
    <strong>Essential cookies (Required)</strong>
    <p>Necessary for website functionality</p>
  </label>

  <label>
    <input type="checkbox" name="analytics" value="analytics">
    <strong>Analytics cookies</strong>
    <p>Help us improve our website by collecting usage data</p>
  </label>

  <label>
    <input type="checkbox" name="marketing" value="marketing">
    <strong>Marketing cookies</strong>
    <p>Show you personalized ads based on your interests</p>
  </label>

  <button type="submit">Save Preferences</button>
  <a href="/privacy-policy">Learn More</a>
</form>
```

**Consent Record Storage:**
```javascript
const consentRecord = {
  userId: 'user123',
  timestamp: new Date().toISOString(),
  consentVersion: '2.0',
  purposes: {
    essential: { granted: true, required: true },
    analytics: { granted: true, purpose: 'Website improvement' },
    marketing: { granted: false, purpose: 'Personalized advertising' }
  },
  ipAddress: '192.168.1.1', // For proof
  userAgent: 'Mozilla/5.0...', // For context
  method: 'explicit_opt_in' // or 'implicit', 'presumed'
};

await saveConsentRecord(consentRecord);
```

#### Cookie Banner (GDPR Compliant)

```html
<div id="cookie-banner" role="dialog" aria-labelledby="cookie-title">
  <h2 id="cookie-title">Cookie Preferences</h2>
  <p>
    We use cookies to enhance your experience. Choose which cookies you
    allow us to use. You can change your preferences at any time.
  </p>

  <button onclick="acceptAll()">Accept All</button>
  <button onclick="rejectNonEssential()">Reject Non-Essential</button>
  <button onclick="showPreferences()">Manage Preferences</button>
</div>

<script>
// Must not load non-essential cookies until consent given
function acceptAll() {
  setConsent({ analytics: true, marketing: true });
  loadAnalyticsCookies();
  loadMarketingCookies();
  hideBanner();
}

function rejectNonEssential() {
  setConsent({ analytics: false, marketing: false });
  hideBanner();
}
</script>
```

### Privacy by Design Principles

#### 1. Data Minimization

**Principle:** Collect only data necessary for specified purpose

**Implementation:**
```javascript
// ❌ Bad: Collecting unnecessary data
const userRegistration = {
  email: req.body.email,
  password: req.body.password,
  fullName: req.body.fullName,
  phoneNumber: req.body.phoneNumber, // Not needed
  dateOfBirth: req.body.dateOfBirth, // Not needed
  address: req.body.address, // Not needed
  socialSecurityNumber: req.body.ssn // Definitely not needed!
};

// ✅ Good: Only essential data
const userRegistration = {
  email: req.body.email,
  password: hashPassword(req.body.password),
  displayName: req.body.displayName // Optional
};
```

#### 2. Purpose Limitation

**Principle:** Use data only for specified, explicit purposes

**Implementation:**
```javascript
// Document and enforce purpose
const dataProcessingPurpose = {
  email: [
    'account_authentication',
    'order_confirmations',
    'password_reset'
  ],
  phoneNumber: [
    'order_delivery_notifications'
    // NOT: 'marketing_calls' (requires separate consent)
  ],
  purchaseHistory: [
    'order_fulfillment',
    'customer_support'
    // NOT: 'targeted_advertising' (requires separate consent)
  ]
};

async function processData(data, purpose) {
  if (!isAllowedPurpose(data.type, purpose)) {
    throw new Error('Purpose not authorized for this data');
  }
  // Proceed with processing
}
```

#### 3. Storage Limitation

**Principle:** Retain data only as long as necessary

**Implementation:**
```javascript
const retentionPolicy = {
  userAccounts: {
    active: 'indefinite',
    inactive: '2 years',
    deleted: '30 days grace period'
  },
  orderRecords: '7 years', // Legal requirement
  supportTickets: '3 years',
  analytics: '26 months',
  marketingData: '1 year or until consent withdrawn'
};

// Automated data deletion
async function enforceRetentionPolicy() {
  const now = new Date();

  // Delete inactive accounts
  await User.deleteMany({
    lastActive: { $lt: subYears(now, 2) },
    status: 'inactive'
  });

  // Anonymize old analytics
  await Analytics.updateMany(
    { createdAt: { $lt: subMonths(now, 26) } },
    { $unset: { userId: 1, ipAddress: 1 } }
  );

  // Delete expired marketing consent
  await MarketingConsent.deleteMany({
    $or: [
      { expiresAt: { $lt: now } },
      { withdrawnAt: { $lt: subDays(now, 30) } }
    ]
  });
}

// Schedule daily
cron.schedule('0 2 * * *', enforceRetentionPolicy);
```

## Security & Compliance Expert

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/security-compliance/SKILL.md#security-compliance-lifecycle,key-security-frameworks-standards -->

### Security & Compliance Lifecycle

#### Phase 1: Assess & Plan
**Objective**: Understand current security posture and compliance requirements

**Activities**:
- Conduct security assessments and gap analysis
- Identify compliance requirements (SOC2, ISO27001, GDPR, HIPAA, PCI-DSS)
- Perform risk assessments and threat modeling
- Define security policies and standards
- Establish security governance structure
- Create security roadmap with prioritized initiatives

**Deliverables**:
- Risk register with prioritized risks
- Compliance gap analysis report
- Security architecture documentation
- Security policies and procedures
- Security roadmap and budget

#### Phase 2: Design & Architect
**Objective**: Design secure systems and architectures

**Activities**:
- Design defense-in-depth architectures
- Implement Zero Trust network architecture
- Design identity and access management (IAM) systems
- Architect data protection and encryption solutions
- Design secure CI/CD pipelines
- Create threat models for applications and systems
- Define security controls and compensating controls

**Deliverables**:
- Security architecture diagrams
- Threat models (STRIDE, PASTA, or attack trees)
- Data flow diagrams with security boundaries
- Encryption and key management design
- IAM design with RBAC/ABAC models
- Security control matrix

#### Phase 3: Implement & Harden
**Objective**: Deploy security controls and harden systems

**Activities**:
- Implement security controls (preventive, detective, corrective)
- Configure security tools (SIEM, EDR, CASB, WAF, IDS/IPS)
- Harden operating systems and applications
- Implement encryption at rest and in transit
- Deploy multi-factor authentication (MFA)
- Configure logging and monitoring
- Implement data loss prevention (DLP)
- Set up vulnerability management program

**Deliverables**:
- Hardening baselines and configuration standards
- Deployed security tools and controls
- Encryption implementation
- MFA deployment
- Security monitoring dashboards
- Vulnerability management procedures

#### Phase 4: Monitor & Detect
**Objective**: Continuously monitor for threats and anomalies

**Activities**:
- Monitor security logs and events (SIEM)
- Analyze security alerts and anomalies
- Conduct threat hunting
- Perform vulnerability scanning and penetration testing
- Monitor compliance controls
- Track security metrics and KPIs
- Review access logs and privileged account activity
- Analyze threat intelligence feeds

**Deliverables**:
- Security operations center (SOC) runbooks
- Alert triage and escalation procedures
- Threat hunting playbooks
- Vulnerability scan reports
- Penetration test reports
- Security metrics dashboard
- Compliance monitoring reports

#### Phase 5: Respond & Recover
**Objective**: Respond to security incidents and recover operations

**Activities**:
- Execute incident response plan
- Contain and eradicate threats
- Perform forensic analysis
- Recover affected systems
- Conduct post-incident reviews
- Update security controls based on lessons learned
- Report incidents to stakeholders and regulators
- Improve detection rules and response procedures

**Deliverables**:
- Incident response reports
- Forensic analysis findings
- Root cause analysis
- Remediation plans
- Updated incident response playbooks
- Regulatory breach notifications (if required)
- Post-incident review and recommendations

#### Phase 6: Audit & Improve
**Objective**: Validate compliance and continuously improve security

**Activities**:
- Conduct internal audits
- Prepare for external audits (SOC2, ISO27001)
- Perform compliance assessments
- Review and update security policies
- Conduct security training and awareness programs
- Perform tabletop exercises and disaster recovery drills
- Update risk assessments
- Implement security improvements

**Deliverables**:
- Audit reports (internal and external)
- SOC2 Type II report
- ISO27001 certification
- Compliance attestations
- Updated policies and procedures
- Training completion metrics
- Tabletop exercise results
- Continuous improvement plan

---

### Key Security Frameworks & Standards

#### NIST Cybersecurity Framework (CSF)
- **Purpose**: Risk-based framework for improving cybersecurity
- **Structure**: 5 Functions, 23 Categories, 108 Subcategories
- **Best for**: General organizations, government contractors
- **Maturity model**: Tier 1 (Partial) to Tier 4 (Adaptive)

#### CIS Critical Security Controls
- **Purpose**: Prioritized set of actions for cyber defense
- **Structure**: 18 Controls with Implementation Groups (IG1, IG2, IG3)
- **Best for**: Practical implementation guidance
- **Focus**: Defense against common attack patterns

#### ISO/IEC 27001
- **Purpose**: International standard for information security management
- **Structure**: 14 domains, 114 controls (Annex A)
- **Best for**: International recognition, formal certification
- **Requirements**: ISMS (Information Security Management System)

#### SOC 2 Type II
- **Purpose**: Service organization controls for security and availability
- **Structure**: Trust Service Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy)
- **Best for**: SaaS companies, cloud service providers
- **Audit**: 3-12 month observation period

#### NIST 800-53
- **Purpose**: Security controls for federal systems
- **Structure**: 20 families, 1000+ controls
- **Best for**: Government contractors, FedRAMP
- **Baselines**: Low, Moderate, High impact systems

#### GDPR (General Data Protection Regulation)
- **Purpose**: EU data privacy regulation
- **Scope**: Any organization processing EU residents' data
- **Requirements**: Lawful basis, consent, data subject rights, breach notification
- **Penalties**: Up to 4% of global revenue or €20M

#### HIPAA (Health Insurance Portability and Accountability Act)
- **Purpose**: Protect health information (PHI)
- **Scope**: Healthcare providers, payers, business associates
- **Requirements**: Administrative, Physical, Technical safeguards
- **Penalties**: $100-$50,000 per violation, criminal charges possible

#### PCI-DSS (Payment Card Industry Data Security Standard)
- **Purpose**: Protect cardholder data
- **Structure**: 12 requirements, 6 control objectives
- **Scope**: Any organization storing, processing, or transmitting card data
- **Levels**: Based on transaction volume (Level 1-4)

---
