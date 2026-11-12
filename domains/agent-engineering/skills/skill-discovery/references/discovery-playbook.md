# Discovery playbook

Adapted by OpenDigital from vercel-labs/skills, skills/find-skills/SKILL.md, commit d3701c11b1101251af14c9d148f026e1a47ebe17 (MIT; see LICENSE.txt). The upstream provides task-specific search, keyword variation, candidate comparison and a no-result fallback. This catalog broadens the discovery beyond one registry and replaces popularity thresholds and global auto-install examples with content/license/host review and scoped approval.

## Original example: an instructional-design request

Start with education/instructional-design in the local catalog. If a missing capability remains, write it as an observable need, such as mapping learning objectives to assessment evidence. Search those terms in candidate source repositories/registries, then read the actual skill and supporting resources at a fixed commit. Check that Bloom labels reflect task demand, that references exist and that no unsafe installer or restricted table is embedded. Record what the candidate adds to the owner instead of creating another generic course-design skill.

## Candidate record

Source URL and commit; file/local license; intended task; host/runtime requirements; scripts/assets/dependencies actually inspected; effects and credential/network requirements; overlap with the local owner; demonstrated checks versus assumptions; recommendation and remaining uncertainty.

If the registry lists a skill but its repository is inaccessible, state that inspection was incomplete. If no matching candidate is found, describe the searched scope and offer direct work or an original spec-backed addition. Do not present “not found here” as proof that none exists anywhere.

Installation is a separate action with a concrete reviewed target and appropriate approval. Online install counts and GitHub stars, if reported at all, need source/date and do not establish safety, effectiveness or license permission.


## Internal lookup examples

Use short queries: `design instrucional`, `taxonomia de Bloom`, `aprender`, `ensinar`, `avaliação da aprendizagem`, `design jurídico` and `Session Lens`. The local command indexes public metadata and curated aliases, without executing a package or scanning installed agents. An absent match is a lexical-search limit, not proof that the capability is absent; browse the domain before proposing a duplicate.
