---
name: clarify
description: "Resolves ambiguous or underspecified areas in project specifications through targeted clarification questions. Use when a spec exists but has unclear decisions that affect architecture, roadmap, or core functionality."
argument-hint: "[spec-file-path or clarification]"
---

# Clarifying Project Specifications

## Overview

Resolve ambiguous or underspecified areas in a project specification through targeted clarification questions. This skill focuses on **high-impact design decisions** that would affect system architecture, roadmap direction, or core functionality -- not trivial options that can be easily added later with no side effects.

**User's Input:** $ARGUMENTS

<HARD-GATE>
Do NOT invoke any implementation skill or start building until high-impact ambiguities are resolved. If critical questions cannot be answered, mark them as BLOCKERS and stop -- do not proceed to implementation with unresolved scope/data/permission questions.
</HARD-GATE>

## When NOT to Ask Questions

Skip clarification for:
- **Trivial choices** -- UI colors, button labels, copy variations, formatting preferences
- **Easily reversible decisions** -- anything that can be changed later without refactoring
- **Implementation details** -- tech stack, libraries, code structure (these are planning-phase decisions)
- **Low-impact uncertainties** -- things that won't materially change the spec's direction

**Exception:** If the user provides a direct clarification in their argument, ALWAYS document it -- regardless of how trivial it may seem. User input takes precedence.

**Rule of thumb:** If the answer won't change the spec's core scope, user scenarios, success criteria, or data model -- don't ask. Note it as a TODO and move on.

## When to Ask Questions

Ask about things that could significantly change the design:
- **Scope boundaries** -- what's explicitly in/out of scope
- **User roles/permissions** -- who can do what
- **Data requirements** -- what entities, relationships, persistence needs
- **Critical flows** -- core user journeys that define the system
- **Success criteria** -- how we measure if it worked
- **Constraints** -- budget, timeline, compliance, integrations
- **Ambiguous terms** -- unclear vocabulary affecting requirements

## The Process

### 1. Handle User Input

Examine `$ARGUMENTS` to determine what the user is providing:

**Case A: User provides a direct clarification or correction**
- The argument is something the user thinks needs clarification or correction -- it may or may not be an answer to a previous question
- Document it in the spec regardless of how trivial it may seem
- User's direct input takes precedence over triviality filtering

**Case B: User provides a spec file path**
- This is a secondary/feature spec, separate from the main project
- Cross-reference with `SPEC.md` at project root for context
- Make all modifications to the user-provided spec file, NOT the main SPEC.md
- The main SPEC.md may reference this secondary spec; note that relationship

**Case C: No argument provided**
- Work with `SPEC.md` at project root
- Ask user if location is unclear

### 2. Load the Specification

Find and read the target spec file:
- If user provided a path: read that file
- If no argument: read `SPEC.md` in project root
- Ask user if location is unclear

### 2.5. Explore Project Context

Before diving into ambiguities, briefly understand the current state:
- Read README.md at project root
- Read the target spec file (as identified in Section 2)
- If user provided a secondary spec: cross-reference with main SPEC.md for context

Do NOT explore the full project codebase -- stay focused on the spec.

### 3. Scan for Ambiguities

Review the spec against this coverage taxonomy. Mark each category as **Clear**, **Partial**, or **Missing**:

| Category | What to Check |
|----------|---------------|
| **Scope** | Core goals, success criteria, out-of-scope explicit |
| **Actors** | User roles, personas, permissions |
| **Data Model** | Entities, attributes, relationships, persistence |
| **User Flows** | Critical journeys, error states, edge cases |
| **Success Metrics** | Measurable outcomes, definition of done |
| **Constraints** | Technical, timeline, compliance, integrations |
| **Terminology** | Clear definitions, consistent usage |

### 4. Prioritize Questions

Only ask questions that meet ALL criteria:
1. Answer would materially change architecture, scope, or roadmap
2. Uncertainty is high (no clear best practice or context missing)
3. Getting it wrong would cause significant rework

**Prioritization heuristic:** `(Impact x Uncertainty)` -- focus on high-impact unknowns.

**Question Limits:**
- Maximum 5 questions per session
- Maximum 10 total questions in a conversation
- **Exception:** Follow-up questions on the same ambiguity may ignore the 5/10 limit -- they are clarifying a single topic, not adding new ones
- **Critical blocking ambiguities** (scope, data model, permissions) may exceed the 10 total limit if needed to unblock development

### 5. Ask One Question at a Time

**Simple questions with follow-ups over complex questions:**
- Break complex ambiguities into multiple simple questions
- Example: Instead of "What data do you need?" ask "What entity types?" -> then "What attributes for users?" -> then "How long to persist?"
- This allows course-correction midstream if early answers change priorities
- If user answer reveals new context, ask a follow-up before moving to next topic
- Only ask 1-2 questions per topic before pausing to present what you've learned

**Format each question:**

1. **State the ambiguity clearly** -- what specifically is unclear
2. **Present recommended option first** -- with 1-2 sentence reasoning
3. **Offer alternatives** -- 2-4 options with trade-offs
4. **Prefer AskUserQuestion** -- use native UI when available
5. **Accept short answers** -- for free-form clarifications

**For multiple-choice:**
```
Recommended: [Option A] - best because [reasoning]

Options:
- A: [Description]
- B: [Description]
- C: [Description]

Or provide your own answer in a few words.
```

**For short-answer:**
```
Suggested: [Proposed answer] - [brief reasoning]

Please answer in a few words or say "yes" to accept.
```

### 6. Integrate Answers Inline

After each answer, update the **target spec file in place** (not just append):

- **Replace ambiguous text** with clarified version
- **Add constraints** to existing sections
- **Refine scope** statements directly
- **Clarify terminology** where it's used
- **Mark resolved TODOs** with the answer

**Important:**
- If user provided a spec file path, modify THAT file -- NOT the main SPEC.md at root
- If user gave a direct clarification in arguments, document it regardless of triviality
- Only create a "Clarifications" appendix if inline update would be awkward

### 7. Present Updated Spec

After resolving questions:
- Show the spec with changes highlighted
- Note which categories were clarified
- Suggest next step (implementation planning or more clarification)

## Question Quality Rules

**Good questions:**
- Have a recommended answer based on context/best practices
- Would change the spec's direction if answered differently
- Can be answered in a few words or one selection
- Target unclear scope, data, roles, or success metrics

**Don't ask:**
- Questions with no clear best answer (just note as TODO)
- Questions where any answer works equally well
- Questions about implementation (defer to planning)
- Questions already answered in context
- Questions the user explicitly said to skip

## Success Criteria

- [ ] Each question has a recommended option with reasoning
- [ ] Questions focus on architecture/roadmap impact
- [ ] Spec updated inline, not just appended
- [ ] Maximum 5 questions per session
- [ ] Trivial ambiguities noted as TODOs, not questions
- [ ] User approves spec before moving to implementation

## Next Steps

After clarifying questions are answered, determine the appropriate next action:

### If Clarifications Greatly Alter Requirements
- The answers change core scope, user scenarios, or data model significantly
- **Action:** Re-run the **specify** skill to update the specification with the new understanding

### If Critical Ambiguities Remain
- High-impact questions could not be answered
- Missing information blocks architecture decisions
- **Action:** Re-run **clarify** to continue addressing critical unknowns

### If Crystal Clear
- All high-impact ambiguities resolved
- Spec has clear scope, data model, and success criteria
- **Action:** Continue to **bootstrap** skill for implementation

### If Minor, Non-Blocking Ambiguities Remain
- Only trivial or low-impact uncertainties left
- Won't affect architecture or core functionality
- **Action:** Present options to user:
  - Continue clarifying if they want
  - Proceed to **bootstrap** if they're ready
