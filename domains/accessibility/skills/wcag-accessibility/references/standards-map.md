# Accessibility and usability standards map

Reference for `accessibility:wcag-accessibility`. Which standard applies, what it covers and how much weight it carries. For WCAG success criteria themselves, use the checklists in this skill; this page places WCAG among the other standards.

Behavioural "laws of UX" are tendencies; the standards below define verifiable criteria that can be used in audits, contracts and specifications. Confirm the current version and the legal reference with the client or counsel before stating that a product is compliant.

## Web and software accessibility

| Standard | Scope | Status and weight |
|---|---|---|
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (W3C) | Web content; applied to apps through WCAG2ICT | W3C Recommendation (2023). Levels A, AA, AAA; AA is the usual contractual and legal target |
| WCAG 3 | Successor model with a different conformance approach | Working draft; do not use for conformance claims |
| ABNT NBR 17225:2025 | Brazilian requirements for accessibility of web content and applications | Brazilian national standard, aligned with WCAG |
| ABNT NBR 17060:2022 | Brazilian requirements for accessibility of mobile applications | Brazilian national standard |
| [eMAG 3.1](https://emag.governoeletronico.gov.br/) | Accessibility model for Brazilian federal government sites | Government guideline, based on WCAG 2.0 |
| EN 301 549 | ICT accessibility in the European Union (web, software, documents, hardware) | Harmonised standard; its web clauses reference WCAG |
| Section 508 (US) | Accessibility of US federal ICT | Legal requirement; references WCAG 2.0 AA |

In Brazil, the Lei Brasileira de Inclusão (Lei 13.146/2015, art. 63) requires accessible websites for companies headquartered or with commercial representation in the country and for public bodies.

### Principles behind WCAG (POUR)

- **Perceivable:** content can be perceived in more than one way (text alternatives, captions, contrast, resizable text).
- **Operable:** every function works by keyboard and other inputs, with enough time and without seizure risks.
- **Understandable:** text is readable, behaviour is predictable, errors are identified and explained.
- **Robust:** content works with assistive technologies and different user agents (valid roles, names, states).

### What WCAG 2.2 added over 2.1

| Criterion | Level | What to check |
|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | Sticky headers, banners and chat widgets do not hide the focused element |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | Focused element fully visible |
| 2.4.13 Focus Appearance | AAA | Focus indicator size and contrast |
| 2.5.7 Dragging Movements | AA | Every drag action has a single-pointer alternative |
| 2.5.8 Target Size (Minimum) | AA | Targets at least 24 × 24 CSS px or spaced, with exceptions |
| 3.2.6 Consistent Help | A | Help mechanisms appear in the same relative place |
| 3.3.7 Redundant Entry | A | Do not ask again for information already given in the same process |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive test (memorising, transcribing) to log in without an alternative; allow paste and password managers |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | No object or personal-content recognition either |

4.1.1 Parsing is obsolete in WCAG 2.2 and no longer required.

## Usability and human-centred design (ISO 9241)

| Part | Topic | Use |
|---|---|---|
| ISO 9241-11:2018 | Definition of usability: effectiveness, efficiency and satisfaction for specified users, goals and context of use | Frame usability requirements and test measures |
| ISO 9241-110:2020 | Interaction principles: suitability for the user's tasks, self-descriptiveness, conformity with user expectations, learnability, controllability, use-error robustness, user engagement | Checklist for interaction design reviews |
| ISO 9241-112:2017 | Principles for the presentation of information | Visual and information design reviews |
| ISO 9241-210:2019 | Human-centred design process: understand the context of use, specify requirements, produce solutions, evaluate against requirements, iterate | Process requirement in contracts and quality systems |

ISO standards are paid documents: cite part and clause, do not reproduce their text.

## Choosing what to cite

- **Audit or contract:** WCAG 2.2 AA plus the local legal reference (ABNT NBR 17225 and LBI in Brazil; EN 301 549 in the EU; Section 508 for US federal work).
- **Brazilian federal service:** eMAG and GOV.BR DS together with WCAG 2.2 AA.
- **Mobile app in Brazil:** ABNT NBR 17060 plus WCAG applied to mobile.
- **Process or quality system:** ISO 9241-210 for the process, ISO 9241-11 for how usability is measured.
