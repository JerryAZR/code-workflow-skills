---
name: spec-create
description: "Creates or updates project specifications. Use when the user wants to start a new project, add a feature, or describes a capability they wish they had."
argument-hint: "[project or feature description]"
---

# Creating Project Specifications

## Overview

Turn vague ideas into a concrete specification document that captures what the project does, who it's for, and how we'll know it worked. This is a living document -- new features are added to it as they are defined.

**User's Intent:** $ARGUMENTS

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, or take any implementation action until you have presented a specification and the user has approved it.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Spec"

Every feature goes through this process. A button, a utility function, a small tool -- all of them. "Simple" features are where unexamined assumptions cause the most wasted work. The spec can be short (a few sentences for truly simple features), but you MUST create one and get approval.

## Checklist

Complete these items in order:

1. **Explore the idea** -- understand what the user is trying to achieve
2. **Capture required decisions** -- get answers to: name, what it does, who it's for, success criteria, primary user scenario
3. **Fill the template** -- write spec to `SPEC.md` in project root
4. **Validate quality** -- check against the quality checklist
5. **Present to user** -- highlight key sections, point out [NEEDS CLARIFICATION] markers
6. **Get approval** -- ask "Does this capture what you're looking for?"
7. **Transition to spec-clarify** -- invoke spec-clarify skill to resolve open questions

## The Process

**Understanding the idea:**
- Listen to what the user wants to achieve
- If unclear on any required decision, ask follow-up questions conversationally
- Present 2-3 options with trade-offs when the user hasn't thought something through
- Ask questions one at a time -- if a topic needs more exploration, break it into multiple questions

**Required decisions to capture:**

| Decision | Description |
|----------|-------------|
| Name | Short, descriptive (1-3 words) |
| What it does | Core functionality from user perspective |
| Who it's for | Target audience (can be brief or inferred) |
| Success criteria | How we'll know it worked (at least 1 measurable outcome) |
| Primary scenario | Main user flow (step-by-step) |

**Filling gaps:**
- Make informed guesses using context and industry standards
- Document assumptions in the spec
- Mark truly ambiguous areas with [NEEDS CLARIFICATION: question] for spec-clarify phase
- **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers in this spec**

## The Specification File

Write to `SPEC.md` in the project root. This is a living document -- add new features to it as they are defined.

**Contents (bullet points):**
- What this program does (one-sentence summary)
- Problem it solves
- Who it's for
- Core functionality (key capabilities)
- User scenarios (primary flows)
- Success criteria (how we know it works)

## Quality Checklist

Before presenting to the user, verify:

- [ ] Has a short, descriptive name
- [ ] Core functionality described (user-facing language)
- [ ] Primary user scenario clearly described
- [ ] At least one measurable success criterion
- [ ] No implementation details (no tech stack, no code, no APIs)
- [ ] Maximum 3 [NEEDS CLARIFICATION] markers

## Success Criteria Guidelines

Success criteria must be:
- **Measurable**: Include specific metrics (time, percentage, count, rate)
- **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
- **User-focused**: Describe outcomes from user/business perspective
- **Verifiable**: Can be tested without knowing implementation details

**Good examples**:
- "Users can complete checkout in under 3 minutes"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (too technical):
- "API response time is under 200ms" -> use "Users see results instantly"
- "Database can handle 1000 TPS" -> use user-facing metric

## After the Spec

**Presentation:**
- Present the spec to the user
- Highlight: name, what it does, who it's for, success criteria
- Point out any [NEEDS CLARIFICATION] markers -- these go to spec-clarify phase
- Ask: "Does this capture what you're looking for?"

**Next step:**
- Upon user approval, invoke the spec-clarify skill to resolve open questions
- Do NOT invoke any implementation skill until spec-clarify is complete

## Key Principles

- **What, not how** -- Describe from user perspective, not implementation
- **Measure success** -- Always include at least one measurable outcome
- **Flag, don't stall** -- Mark ambiguities with [NEEDS CLARIFICATION] rather than endless questions
- **Get approval** -- Don't proceed to implementation without user sign-off
- **Short is fine** -- A simple feature gets a simple spec
