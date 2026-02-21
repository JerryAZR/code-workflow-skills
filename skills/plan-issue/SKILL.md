---
name: plan-issue
description: "Use when an issue document exists and needs a task roadmap with TDD discipline"
argument-hint: "[issue-number or issue-slug]"
---

# Plan Issue

## Overview

Create an actionable task roadmap for resolving an issue using TDD (Test-Driven Development) workflow.

**User's Intent:** $ARGUMENTS

Emphasizes **failing tests first** principle.

## Prerequisites

- Issue document exists in `issues/` directory

## Workflow

1. **Select Issue** - Find the issue (latest if not specified)
2. **Analyze Issue** - Read expected behavior, current behavior, architecture impact
3. **Create Tasks** - Generate task roadmap with TDD emphasis
4. **Output** - Write tasks to issue document

---

## Step 1: Select Issue

If specified: find `issues/<issue-number>-*.md` or `issues/*-<slug>.md`

If not: find latest issue by highest numeric prefix.

**Error:** If no issues exist, report: "Create an issue first using new-issue skill."

---

## Step 2: Analyze Issue

Extract: Expected Behavior, Current Behavior, Architecture Impact, Priority, Testing needs

---

## Step 3: Create Tasks

Generate task roadmap following this structure:

### Task Format

`- [ ] [TaskID] [P?] [Phase] Description`

- `[P]`: parallelizable (different files)
- Phase: SPC, ARC, FND, TST, IMPL, POL

---

### Phase Structure

| Phase | Purpose | When to Include |
|-------|---------|-----------------|
| SPC | SPEC Update | New requirements |
| ARC | Architecture | Structural changes |
| FND | Foundational | Data model, deps |
| TST | Tests | Always - write failing first |
| IMPL | Implementation | Always |
| POL | Polish | Docs, cleanup |

**TDD Discipline:** Tests MUST fail (red) before implementation. Write tests that define desired behavior, not exception tests.

---

### Task Generation Rules

- TDD First: tests before implementation
- Fail Before Pass: verify tests fail first
- Minimal: only what's needed to pass tests
- SPC/ARC optional: skip if not needed

---

## Step 4: Output

Append tasks to issue document using task format. Order: FND → TST → IMPL → POL

---

## Constraints

- Do NOT implement - only create roadmap
- Tests before implementation (TDD)
- Tests must fail initially (red state)

## Quick Reference

| Phase | Purpose | Key Action |
|-------|---------|------------|
| SPC | SPEC Update | Add new requirements to SPEC.md |
| ARC | Architecture | Update node docs |
| FND | Foundational | Data model, dependencies |
| TST | Tests | Write failing tests first |
| IMPL | Implementation | Make tests pass |
| POL | Polish | Docs, cleanup |

## Example

Issue: "Add dark mode to settings page"

```
- [ ] T001 [SPC] Add to SPEC.md
- [ ] T010 [FND] Add theme to config/
- [ ] T013 [TST] Write failing test in tests/ui/
- [ ] T016 [IMPL] Add theme context
- [ ] T019 [POL] Update docs
```

## Next Steps

After planning:
- **Execute**: Run `resolve-issue` to implement the tasks in order
- **Iterate**: Use plan-issue again if scope changes
