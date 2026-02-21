---
name: milestone-test-add
description: "Implements additional tests for nodes with state 'modified'. Use when a parent node's implementation modified a child node's behavior, requiring additional test coverage before milestone-integrate."
argument-hint: "[node-name]"
---

# Milestone Test Add

## Overview

Implement additional functional tests for nodes with state "modified". Nodes become "modified" when their parent node's implementation changes or extends the child's behavior during node-build. These tests verify the new/modified functionality and should pass (green) because the functionality already exists.

This skill adds test coverage for behavioral changes introduced during implementation, complementing the initial tests created during node-prep.

**User's Intent:** $ARGUMENTS

If no node-name provided, find all eligible modified nodes automatically.

## Prerequisites

- `arch/ARCH_SUMMARY.md` exists with architecture tree
- Nodes with state `modified` exist (set during node-build when parent modifies child)
- Node implementation exists at `src/<node_path>.py`
- Initial tests exist at `tests/<node_path>.py`
- Run `node-build` first to implement nodes and create modified states

## Node State Model

| State | Meaning |
|-------|---------|
| `pending` | Awaiting contract definition (architecture phase) |
| `atomic` | Leaf node in architecture (architecture phase) |
| `decomposed` | Non-leaf node in architecture (architecture phase) |
| `planned` | Node has milestone contract, awaiting preparation |
| `prepared` | Skeleton + failing tests created |
| `implemented` | Logic implemented and tests passing |
| `modified` | Parent implementation changed this node's behavior; needs additional tests |

## Workflow

Follow this process in order:

1. **Find Modified Nodes** - Locate all nodes with state "modified"
2. **Understand Node Changes** - Read what changes parent made to this node
3. **Generate Tests** - Create additional functional tests for the modifications
4. **Run Tests** - Verify tests pass (green state)
5. **Fix Issues** - If tests fail, fix test or implementation
6. **Update State** - Transition node to "implemented"

---

## Step 1: Find Modified Nodes

### If node-name provided:

Verify the node exists in `arch/ARCH_SUMMARY.md` and has state `modified`.

### If no node-name provided:

Find all eligible nodes:

1. Parse `arch/ARCH_SUMMARY.md`
2. Collect all nodes where State == `modified`
3. Process all found nodes (can be done in parallel)

**Error Handling:**
- If no nodes with state "modified" exist, report: "No modified nodes found. All nodes are either implemented or not yet modified. Run node-build to implement nodes, which may set children to 'modified' state."

---

## Step 2: Understand Node Changes

Read the node's documentation to understand what was modified:

1. Read `arch/nodes/<NodePath>.md` for structural contract
2. Read the current implementation at `src/<node_path>.py`
3. Check any notes in `arch/ARCH_SUMMARY.md` about why node was marked modified

**Key Question:** What did the parent implementation change about this node's behavior?

Common modification scenarios:
- Parent now calls additional methods on child
- Parent expects different return format from child
- Parent passes additional parameters to child
- Child behavior was extended to support parent needs

---

## Step 3: Generate Tests

Generate additional functional tests that verify the modified behavior.

### Critical: Real Functional Tests vs Structural Tests

Tests must define desired behavior — not confirm absence of implementation.

```
✅ CORRECT (functional test):
assert calculate_total([10, 20, 30]) == 60
assert process_user_input("") raises ValueError

❌ WRONG (structural test):
assert MyClass is not None
assert my_method is callable
```

### Test Requirements

Generate tests that:

- **Target public interface only** - Test public methods, not internal implementation
- **Cover all scenarios**:
  - Nominal behavior (happy path)
  - Edge cases
  - Failure semantics (verify functions raise appropriate errors like ValueError, TypeError)
  - Invariants
- **Express real input/output expectations** - Test actual behavior, not structure

### Explicitly Forbidden Test Patterns

Do NOT generate any of these:

1. **NotImplementedError-expecting tests** - Tests that assert methods throw NotImplementedError or NotImplementedException
2. **Structural validation tests** - Tests that only check:
   - Object instantiation
   - Method existence
   - Mock wiring behavior
   - Interface shape validation
3. **Integration tests** - Tests spanning multiple nodes or external systems

### File Path Convention

**Existing test file:** `tests/<node_path>.py` (e.g., `tests/auth/test_user_validator.py`)

**Append new tests** to the existing test file. Do NOT create new test files.

### Test Function Naming

- `test_<method>_<expected_behavior>`
  - e.g., `test_validate_email_returns_true_for_valid_email`
  - e.g., `test_validate_email_raises_error_for_empty_string`
- **Group by functionality**: Happy path, error handling, edge cases

---

## Step 4: Run Tests

Execute the tests to verify they pass:

```bash
pytest tests/<node_path>.py -v
```

**Expected Result:** All tests PASS (green state)

The tests should pass because:
- The functionality being tested already exists
- The implementation is correct
- The tests verify the modified behavior accurately

---

## Step 5: Fix Issues

If tests FAIL:

1. **Analyze failure**: Is the test wrong, or is the implementation wrong?
2. **If test is wrong**: Fix the test to correctly verify the expected behavior
3. **If implementation is wrong**: Fix the implementation to correctly provide the expected behavior

**Iterate** until all tests pass.

---

## Step 6: Update State

In `arch/ARCH_SUMMARY.md`, change the node's status:

```
modified → implemented
```

The node now has complete test coverage for its current milestone contract.

---

## Constraints

### What This Skill Does

- Adds functional test coverage for modified node behavior
- Ensures tests pass (green state)
- Updates node state to "implemented"

### What This Skill Does NOT Do

- Modify node implementation (except to fix bugs found during testing)
- Create new nodes or modify architecture
- Handle nodes that are not "modified"
- Remove or modify existing tests

---

## Success Criteria

- [ ] All modified nodes identified
- [ ] Node changes understood
- [ ] Additional functional tests generated
- [ ] Tests pass (green state)
- [ ] Node state updated to "implemented"

## Next Steps

After adding tests for modified nodes:
- **Integration tests**: Run `milestone-integrate` to create integration tests
- **Wrap up milestone**: Run `milestone-wrapup` for manual verification
