---
name: issue-resolve
description: "Executes issue resolution by processing tasks in batches with review checkpoints. Use when an issue document with task roadmap exists and needs to be resolved with TDD workflow."
argument-hint: "[issue-number or issue-slug]"
---

# Resolve Issue

## Overview

Execute issue resolution by processing tasks from the issue's task roadmap in batches with human review checkpoints between batches.

**User's Intent:** $ARGUMENTS

This skill adapts batch execution patterns with human review checkpoints and TDD discipline.

## Prerequisites

- Issue document exists in `issues/` directory
- Issue document contains a task roadmap (from issue-plan skill)

## Workflow

Follow this process in order:

1. **Load Issue** - Find and read the issue with task roadmap
2. **Analyze Tasks** - Parse task structure, phases, and dependencies
3. **Execute Batch** - Process first batch of tasks
4. **Report Progress** - Show completed work, wait for feedback
5. **Continue or Complete** - Process next batch or finish

---

## Step 1: Load Issue

### If issue specified:

Find `issues/<issue-number>-*.md` or `issues/*-<slug>.md`

### If no issue specified:

Find the latest issue by:
1. List all `.md` files in `issues/` directory
2. Parse numeric prefix (e.g., `001-`, `002-`)
3. Sort by prefix number descending
4. Select first file that contains "Task Roadmap" section

**Error Handling:**
- If no issues exist, report: "No issues found. Create an issue first using issue-create skill."
- If issue has no task roadmap, report: "Issue has no task roadmap. Run issue-plan skill first to generate tasks."

---

## Step 2: Analyze Tasks

Parse the task roadmap from the issue document:

1. **Extract phases** - SPC, ARC, FND, TST, IMPL, POL
2. **Identify dependencies** - Sequential vs parallel execution
3. **Determine batch size** - Default: 2 phases per batch
4. **Check TDD order** - Verify test tasks (TST) come before implementation (IMPL)

### Phase Dependencies

```
FND → TST → IMPL → POL
SPC → (any)
ARC → (any)
```

**Verification:**
- Confirm TST phase tasks exist before IMPL phase
- Confirm FND tasks are listed before TST tasks

---

## Step 3: Execute Batch

**Default batch size: 2 phases**

For each task in the batch:
1. Mark task as in_progress in issue document
2. Execute the task
3. Run verification as specified
4. Mark task as completed with [X]

### Batch Execution Rules

1. **Complete phase before moving on** - Don't skip within a phase
2. **Parallel tasks [P] can run together** - Different files, no dependencies
3. **Sequential tasks must run in order** - Same file or dependent
4. **TDD enforcement**:
   - TST tasks must complete before IMPL tasks begin
   - Tests must fail (red state) before implementation
   - Implementation must make tests pass (green state)

### TDD Workflow Within Batch

```
Phase TST (if in batch):
├── T013 [P] [TST] Write failing tests
├── T014 [P] [TST] Write failing tests
└── T015 [TST] Verify tests FAIL (red state)

Phase IMPL (if in batch):
├── T016 [P] [IMPL] Implement to pass tests
├── T017 [IMPL] Run tests - verify PASS (green state)
└── T018 [IMPL] Refactor if needed
```

---

## Step 4: Report Progress

When batch complete:

1. **Show completed tasks** - List with [X] markers
2. **Show verification output** - Test results, build status
3. **Show remaining tasks** - What's left in roadmap
4. **Say: "Ready for feedback."**

### Progress Report Format

```markdown
## Batch Complete

### Completed
- [X] T010 [FND] ...
- [X] T013 [P] [TST] ... (tests fail as expected)
- [X] T015 [TST] Verify tests FAIL

### Remaining
- [ ] T016 [P] [IMPL] ...
- [ ] T017 [IMPL] ...
- [ ] T019 [P] [POL] ...

Ready for feedback.
```

---

## Step 5: Continue or Complete

Based on user feedback:

**Continue:**
- Execute next batch (next 2 phases)
- Apply any corrections from feedback

**Complete:**
- Mark all remaining tasks as done if issue is resolved
- Show final summary

---

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails unexpectedly)
- Task has unclear instructions
- Verification fails repeatedly
- Issue scope changes

**Ask for clarification rather than guessing.**

---

## Task Marking Convention

Update issue document to track progress:

```markdown
## Task Roadmap

### Phase FND: Foundational

- [X] T010 [FND] Update data model if needed
- [X] T011 [FND] Add required dependencies
- [ ] T012 [P] [FND] Create database migrations if needed

### Phase TST: Tests (TDD - FAILING FIRST)

- [X] T013 [P] [TST] Write unit test for expected behavior
- [ ] T014 [P] [TST] Write integration test for user journey
```

---

## Constraints

- Do NOT execute if task roadmap is incomplete
- Do NOT skip TDD order (tests before implementation)
- Do NOT weaken tests to make them pass
- Do NOT modify task roadmap without user approval

---

## Success Criteria

- [ ] Issue selected (specified or latest with roadmap)
- [ ] Tasks analyzed for phase dependencies
- [ ] Batch executed with TDD discipline
- [ ] Progress reported between batches
- [ ] Tasks marked with [X] as completed
- [ ] Stopped when blocked, asked for clarification

## Next Steps

After issue resolution:
- **Verify**: Run full test suite
- **Review**: Check all tasks completed
- **Close**: Issue can be marked as resolved
