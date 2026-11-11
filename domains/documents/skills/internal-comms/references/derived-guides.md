# Internal communications — derived guides

Part of `documents:internal-comms`.

## Email Composer

<!-- source: davila7/claude-code-templates cli-tool/components/skills/enterprise-communication/email-composer/SKILL.md#common-email-types -->

### Common email types

#### Request for information

```
Subject: Question about Q4 project timeline

Hi [Name],

I hope this email finds you well. I'm reaching out regarding the Q4 product launch timeline.

Could you provide an update on:
- Current progress on feature development
- Expected completion date for testing phase
- Any blockers or dependencies we should be aware of

This will help us coordinate with the marketing team for the launch materials.

Thanks in advance for your help!

Best regards,
[Your name]
```

#### Follow-up email

```
Subject: Following up: Proposal for new payment system

Hi [Name],

I wanted to follow up on the payment system proposal I sent last week. I understand you're busy, so I wanted to make sure it didn't get lost in your inbox.

To recap, the proposed system would:
- Reduce transaction fees by 30%
- Integrate with existing accounting software
- Improve customer checkout experience

I'd be happy to schedule a brief call to discuss any questions you might have.

Looking forward to hearing from you.

Best,
[Your name]
```

#### Technical update

```
Subject: API Maintenance Window - [Date]

Team,

This is a reminder that we'll be performing scheduled maintenance on our API infrastructure on [Date] from [Time] to [Time] [Timezone].

During this window:
- API endpoints will be unavailable
- Database will be upgraded to v14
- SSL certificates will be renewed

Expected downtime: 2 hours

What you need to do:
- Notify your users of the planned downtime
- Ensure retry logic is in place for API calls
- Monitor your application after maintenance completes

If you have any concerns or conflicts with this schedule, please let me know by [Date].

Technical details available in our status page: [link]

Thanks,
[Your name]
```

#### Customer support

```
Subject: Re: Issue with order #12345

Hi [Customer name],

Thank you for reaching out about your order. I'm sorry to hear you're experiencing this issue.

I've looked into your order (#12345) and found the following:

[Explanation of the issue]

To resolve this, I've:
- [Action taken 1]
- [Action taken 2]

You should see [expected outcome] within [timeframe].

If you continue to experience any problems, please don't hesitate to reply to this email or call us at [phone number].

We appreciate your patience and understanding.

Best regards,
[Your name]
Customer Support Team
```

#### Meeting request

```
Subject: Meeting request: Discuss database migration strategy

Hi [Name],

I'd like to schedule a meeting to discuss our approach for the upcoming database migration.

Agenda items:
- Review migration timeline and milestones
- Discuss rollback strategy
- Identify potential risks and mitigation plans
- Assign team responsibilities

Estimated duration: 45 minutes

I'm available:
- Monday 2-4 PM
- Wednesday 10 AM - 12 PM
- Friday 1-3 PM

Please let me know what works best for you, or feel free to suggest alternative times.

Best,
[Your name]
```

## Feedback Conversations

<!-- source: davila7/claude-code-templates cli-tool/components/skills/enterprise-communication/feedback-mastery/SKILL.md#common-difficult-scenarios,preparation-phase,sbi-examples-for-software-teams -->

### Preparation Phase

#### Step 1: Understand the Issue

Ask yourself:

- **What exactly is the problem?** (Be specific, not vague)
- **How does it impact the team, project, or company?**
- **Have I gathered all relevant facts?**
- **Is this a pattern or a one-time event?**

#### Step 2: Define Your Goals

Before the conversation, clarify what you're seeking:

| Goal Type | Example |
| --- | --- |
| Behavior change | "I want them to submit code reviews on time" |
| Mutual understanding | "I want to understand what's blocking them" |
| Expectation setting | "I want to clarify what 'done' means for features" |
| Problem solving | "I want to find a solution together" |

**Tip:** Use if-then statements to clarify stakes:
> "If this behavior continues, then the project timeline will suffer, leading to missed deliverables."

#### Step 3: Manage Your Emotions

High emotional intensity reduces cognitive processing by 30%. Before the conversation:

- [ ] Am I calm and in control?
- [ ] Have I separated facts from personal frustrations?
- [ ] Have I considered their perspective?
- [ ] Can I present this without accusation?

**Reframing technique:**

| Accusatory | Constructive |
| --- | --- |
| "You always miss deadlines and it slows everyone down" | "I've noticed some recent delays and want to understand any challenges you're facing" |
| "You never test your code properly" | "I've seen a few bugs slip through recently. Let's talk about our testing process" |

### SBI Examples for Software Teams

#### Positive Feedback

**Code Review:**
> **Situation:** "During Tuesday's code review for the authentication module..."
> **Behavior:** "...you provided detailed comments on potential security vulnerabilities and suggested efficient fixes..."
> **Impact:** "...which strengthened our security posture and saved the team hours of debugging later."

**Collaboration:**
> **Situation:** "In yesterday's architecture discussion..."
> **Behavior:** "...you asked clarifying questions and built on others' ideas instead of pushing your own solution..."
> **Impact:** "...which helped us reach consensus faster and made everyone feel heard."

#### Constructive Feedback

**Missed Deadlines:**
> **Situation:** "When we were finalizing the API deployment last Thursday..."
> **Behavior:** "...your testing results came in two hours after our agreed cutoff..."
> **Impact:** "...which delayed the release, risked our SLA, and caused the QA team to work overtime."

**Meeting Behavior:**
> **Situation:** "In our sprint planning yesterday..."
> **Behavior:** "...you were on your phone for most of the discussion and didn't contribute when we asked for estimates..."
> **Impact:** "...which left the team without your expertise on the backend stories and made others feel their time wasn't valued."

**For more examples:** See `references/feedback-sbi-model.md`

### Common Difficult Scenarios

#### Scenario: Performance Issue

**Situation:** A developer consistently delivers code with bugs.

**Approach:**

1. **Prepare:** Gather specific examples (PRs, bug counts, timelines)
2. **Deliver:** "I've noticed [X bugs in last Y PRs]. I want to understand what's happening and how I can support you."
3. **Explore:** Ask about workload, clarity of requirements, testing confidence
4. **Collaborate:** "What would help you feel more confident about code quality?"
5. **Follow-up:** Check in after agreed changes, recognize improvements

#### Scenario: Conflict Between Team Members

**Situation:** Two engineers disagree on technical approach and it's affecting the team.

**Approach:**

1. **Meet separately first:** Understand each perspective
2. **Find common ground:** What do they both want? (Working product, good code, etc.)
3. **Facilitate together:** Focus on facts and trade-offs, not personalities
4. **Establish decision process:** How will the team decide when there's disagreement?
5. **Follow-up:** Check that the solution is working

#### Scenario: Unrealistic Expectations

**Situation:** Leadership wants a feature in half the time needed.

**Approach:**

1. **Prepare:** Data on similar past work, breakdown of required tasks
2. **Deliver:** "I want to make sure we're aligned on what's realistic. Here's what I'm seeing..."
3. **Present trade-offs:** "We can hit that date if we [reduce scope/add people/accept risk]"
4. **Collaborate:** "What's most important here - the date or the full feature set?"
5. **Document:** Get agreement in writing to avoid future misalignment

**For detailed scripts:** See `references/difficult-conversation-scripts.md`

## Difficult Conversations Skill

<!-- source: davila7/claude-code-templates cli-tool/components/skills/enterprise-communication/difficult-workplace-conversations/SKILL.md#example-scenarios -->

### Example Scenarios

#### Scenario 1: Addressing Missed Deadlines

```markdown
**Issue:** Team member missed 3 deadlines in past month
**Impact:** Project delayed, others blocked
**Goal:** Understand root cause, agree on prevention plan

**Opening:** "I wanted to check in about the recent deliverables. I've noticed
the last three have come in past deadline, and I'd like to understand what's
happening and how we can address it together."
```

#### Scenario 2: Peer Conflict

```markdown
**Issue:** Colleague publicly criticized your work in meeting
**Impact:** Embarrassed, trust damaged
**Goal:** Address behavior, rebuild working relationship

**Opening:** "I'd like to talk about what happened in yesterday's standup.
When you said my code 'missed obvious issues,' I felt called out in front
of the team. I'd like to understand your concerns and find a better way
to handle code quality feedback."
```

#### Scenario 3: Asking Manager for Raise

```markdown
**Issue:** Feel underpaid relative to market/contribution
**Impact:** Demotivation, considering leaving
**Goal:** Discuss compensation, get timeline or adjustment

**Opening:** "I'd like to discuss my compensation. I've been here two years,
taken on the payments project leadership, and want to make sure my salary
reflects my contributions and the current market."
```

## Professional Communication

<!-- source: davila7/claude-code-templates cli-tool/components/skills/enterprise-communication/professional-communication/SKILL.md#technical-vs-non-technical-communication -->

### Technical vs Non-Technical Communication

#### When to Be Technical vs Accessible

| Audience | Approach |
| --- | --- |
| **Engineering peers** | Technical details, code examples, architecture specifics |
| **Technical managers** | Balance of detail and high-level impact |
| **Non-technical stakeholders** | Business impact, analogies, outcomes over implementation |
| **Customers** | Plain language, what it means for them, avoid jargon |

#### Three Strategies for Simplification

1. **Start with the big picture before details** - People process "why" before "how"
2. **Simplify without losing accuracy** - Use analogies; replace jargon with plain language
3. **Know when to switch** - Read the room; adjust based on questions and engagement

#### Jargon Translation Examples

| Technical | Plain Language |
| --- | --- |
| "Microservices architecture" | "Our system is split into smaller, independent pieces that can scale separately" |
| "Asynchronous message processing" | "Tasks are queued and processed in the background" |
| "CI/CD pipeline" | "Automated process that tests and deploys our code" |
| "Database migration" | "Updating how our data is organized and stored" |

**For more examples**: See `references/jargon-simplification.md`
