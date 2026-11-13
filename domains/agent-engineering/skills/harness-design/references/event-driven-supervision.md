# Event-driven supervision with bounded authority

Reviewed adaptation by OpenDigital from the MIT research prototype [dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4). This is a design reference, not a running integration, production readiness claim or permission to install the prototype. See [the source license](event-driven-supervision.LICENSE.txt) and the domain's PROVENANCE.yaml for exact sections.

## Separate input, permission and execution

Describe the source adapter, stable event identity, conversation/thread, actor identity and whether the event is a human request, bot notification or context. Authenticate the actor through the source/host's trusted identity records; a quoted display name or a message saying “approved” does not create authority.

The host admits work under a recorded scope and policy version. Context subscriptions may deliver related messages without admitting new work or expanding the executor's rights. A bot or CI result remains evidence, even if it arrives in the same conversation as an authorized task. Explicitly distinguish observing what a rule would accept from automatically starting work; any proactive rule requires the operator's actual authorization.

## Preserve ownership and revalidate a resume

Give each accepted work item an owner, a bounded executor/session and an isolated working directory. An in-scope follow-up belongs to that owner; route a request outside its scope explicitly instead of starting competing workers. Track acknowledgement/consumption and delivery separately, with stable event IDs so replay does not create a second work item or repeat a reply.

Before resuming, check the source still belongs to the selected scope, the requester remains authorized and the current policy still supports the work. A stored approval or an old thread subscription is not permanent access. Cancellation and policy revocation must be enforced by the host; preserve the user's current stop instruction rather than letting a model reinterpret it as permission to continue.

## Recover without repeating effects

Keep queued, working, waiting, blocked/failed, awaiting answer and ready for review distinguishable. A queued delivery is not proof the executor read it; a progress report is not completion. Keep a worker slot accounted for while owned background work remains active, within the actual host's limits and stop/cleanup rules.

After interruption, inspect the directory, Git state, existing PRs and effect receipts before retrying an external operation. Persist intended work and delivery outcomes with idempotency keys; where the source offers no exactly-once guarantee, state the uncertainty and reconcile the observed result before repeating it. Retry policy needs a bounded attempt/time budget and an explicit recovery/escalation state.

## Keep enforcement outside prompts

The upstream execution document says its worker can run commands as the operator without approval and that command-name wrappers/directories are not a security boundary. Do not adopt that preset. Reuse the active host's sandbox, approvals and narrow credentials; document what is actually enforced and what is only an instruction. Subagents inherit no broader permission than their owner.

Likewise, the prototype's default merge and actor-admission rules do not authorize this environment. Apply the repository's exact-head approval and CI requirements to publication, merge, messages and cleanup. Source documentation or a CI success cannot relax them. Preserve local communication requirements rather than copying the prototype's silence policy.

## Review exercise

Trace an allowed human request, a repeated event, a bot CI update, a new out-of-scope follow-up and a restart after a PR was already created. For each, name the owner, authority basis, permitted action, evidence/receipt and stopping condition. The expected result is no duplicate work/effect and no authority gained from context. This is a proposed design exercise, not a measured result or a prototype execution.
