---
name: plan-issue
description: "Creates an actionable task roadmap for resolving an issue using TDD workflow. Use when an issue doc exists and needs a task breakdown with failing-tests-first approach."
argument-hint: "[issue-number or issue-slug]"
---

# Plan Issue

## Overview

Create an actionable task roadmap for resolving an issue using TDD (Test-Driven Development) workflow.

**User's Intent:** $ARGUMENTS

This skill adapts the proven tasks.md workflow for issue resolution, emphasizing **failing tests first** principle.

## Prerequisites

- Issue document exists in `issues/` directory

## Workflow

Follow this process in order:

1. **Select Issue** - Find the issue to plan (latest if not specified)
2. **Analyze Issue** - Read expected behavior, current behavior, architecture impact
3. **Create Tasks** - Generate task roadmap with TDD emphasis
4. **Output** - Write tasks to issue document

---

## Step 1: Select Issue

### If issue specified:

Find `issues/<issue-number>-*.md` or `issues/*-<slug>.md`

### If no issue specified:

Find the latest issue by:
1. List all files in `issues/` directory
2. Parse numeric prefixes
3. Select highest number

**Error Handling:**
- If no issues exist, report: "No issues found. Create an issue first using new-issue skill."

---

## Step 2: Analyze Issue

Read the issue document and extract:

1. **Expected Behavior** - What should happen (criteria of success)
2. **Current Behavior** - What happens now (for bugs)
3. **Architecture Impact** - Which nodes are affected
4. **Priority** - Address now or defer
5. **Testing** - What tests are needed

---

## Step 3: Create Tasks

Generate task roadmap following this structure:

### Task Format (REQUIRED)

```
- [ ] [TaskID] [P?] [Phase] Description with file path
```

**Format Components:**

1. **Checkbox**: `- [ ]`
2. **Task ID**: Sequential (T001, T002...)
3. **[P] marker**: Parallelizable (different files, no dependencies)
4. **[Phase]**: SPC (SPEC), ARC (architecture), FND (foundational), TST (tests), IMPL (implementation), POL (polish)
5. **Description**: Action with exact file path

---

### Phase Structure

#### Phase SPC: SPEC Update (Optional)

**Skip if issue does not introduce new requirements or features.**

Update SPEC.md if the issue introduces new functional requirements:

```
- [ ] T001 [P] [SPC] Add new user story to SPEC.md
- [ ] T002 [SPC] Update acceptance criteria in SPEC.md
```

#### Phase ARC: Architecture Update (Optional)

**Skip if issue does not affect architecture.**

Update architecture documents if the issue requires structural changes:

```
- [ ] T003 [P] [ARC] Update ARCH_SUMMARY.md if node states/relationships change
- [ ] T004 [ARC] Create new node docs in arch/nodes/ if new components needed
- [ ] T005 [ARC] Update existing node docs if contracts change
```

#### Phase FND: Foundational

Core changes required before implementation

```
- [ ] T010 [FND] Update data model if needed
- [ ] T011 [FND] Add required dependencies
- [ ] T012 [P] [FND] Create database migrations if needed
```

#### Phase TST: Tests (TDD - FAILING FIRST) ⚠️

**CRITICAL: Write failing tests BEFORE implementation**

```
- [ ] T013 [P] [TST] Write unit test for expected behavior in tests/...
- [ ] T014 [P] [TST] Write integration test for user journey in tests/...
- [ ] T015 [TST] Verify tests FAIL (red state)
```

**TDD Discipline:**
- Tests MUST fail because behavior is missing
- Tests MUST NOT pass in red state
- Do NOT write tests that expect exceptions
- Write tests that define desired behavior

#### Phase IMPL: Implementation

Implement to make tests pass

```
- [ ] T016 [P] [IMPL] Implement feature in src/...
- [ ] T017 [IMPL] Run tests - all should PASS (green state)
- [ ] T018 [IMPL] Refactor if needed - tests remain green
```

#### Phase POL: Polish

Cross-cutting concerns after implementation

```
- [ ] T019 [P] [POL] Update documentation
- [ ] T020 [POL] Run full test suite
- [ ] T021 [POL] Code review and cleanup
```

---

### Task Generation Rules

1. **TDD First**: Test tasks come BEFORE implementation tasks
2. **Test Location**: Match architecture hierarchy (`tests/<node_path>.py`)
3. **Fail Before Pass**: Verify tests fail before implementing
4. **Minimal Implementation**: Only what's needed to pass tests
5. **Optional Phases**: Include SPC (SPEC) and ARC (Architecture) phases only if applicable - skip if not needed

---

## Step 4: Output

Update the issue document by appending:

```markdown
---

## Task Roadmap

### Phase SPC: SPEC Update (Optional - include if new requirements)

- [ ] T001 [P] [SPC] ...

### Phase ARC: Architecture Update (Optional - include if structural changes)

- [ ] T003 [P] [ARC] ...
- [ ] T004 [ARC] ...
- [ ] T005 [ARC] ...

### Phase FND: Foundational

- [ ] T010 [FND] ...

### Phase TST: Tests (TDD - Write Failing First)

- [ ] T013 [P] [TST] ... (ensure FAIL)
- [ ] T015 [TST] Verify tests FAIL

### Phase IMPL: Implementation

- [ ] T016 [P] [IMPL] ...
- [ ] T017 [IMPL] Run tests - ensure PASS

### Phase POL: Polish

- [ ] T019 [P] [POL] ...

## Execution Order

1. (Optional) Complete SPEC Update (SPC) - if new requirements
2. (Optional) Complete Architecture Update (ARC) - if structural changes
3. Complete Foundational (FND)
4. Write failing tests (TST) - verify red state
5. Implement (IMPL) - verify green state
6. Polish (POL)

**Skip SPC/ARC phases if not applicable to this issue.**
```

---

## Constraints

- Do NOT implement code - only create task roadmap
- Tests MUST be written before implementation (TDD)
- Each test must fail initially (red state)
- Use hierarchical test paths matching architecture

---

## Success Criteria

- [ ] Issue selected (specified or latest)
- [ ] Issue analyzed completely
- [ ] Tasks generated in correct phase order
- [ ] Test tasks precede implementation tasks
- [ ] TDD discipline emphasized
- [ ] Task format follows `[ID] [P?] [Phase] Description`

## Next Steps

After planning:
- **Execute**: Run `resolve-issue` to implement the tasks in order
- **Iterate**: Use plan-issue again if scope changes
