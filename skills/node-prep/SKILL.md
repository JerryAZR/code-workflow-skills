---
name: node-prep
description: "Use when milestone-init has been run and nodes have state 'planned' - generates skeleton and failing tests. Requires milestone-init first to set up node contracts."
argument-hint: "[node-name]"
---

# Node Preparation

## Overview

Prepare one implementation-ready node by generating failing functional tests for new capabilities and adding skeleton placeholders where needed, then transitioning the node state to "prepared".

This skill handles both new nodes and existing nodes from past milestones:
- **New nodes**: Create skeleton with NotImplementedError placeholders + failing tests
- **Existing nodes**: Keep existing implementation, add placeholders only for new methods, add failing tests for new capabilities

This skill does not implement logic — it only creates the foundation for implementation.

**User's Intent:** $ARGUMENTS

If no node-name provided, find an eligible node automatically.

## Prerequisites

- `arch/ARCH_SUMMARY.md` exists with architecture tree
- Nodes with state `planned` exist (set by `milestone-init`)
- Run `milestone-init` first to derive node contracts

## Node State Model

| State | Meaning |
|-------|---------|
| `pending` | Awaiting contract definition (architecture phase) |
| `atomic` | Leaf node in architecture (architecture phase) |
| `decomposed` | Non-leaf node in architecture (architecture phase) |
| `planned` | Node has milestone contract, awaiting preparation |
| `prepared` | Skeleton + failing tests created |
| `implemented` | Logic implemented and tests passing |

**Note:** After `milestone-init`, nodes with contracts are set to `planned`. This skill prepares `planned` nodes.

## Workflow

Follow this process in order:

1. **Select Node** - Find eligible node or use provided name
2. **Verify Eligibility** - Confirm node can be prepared
3. **Generate Skeleton** - Create structural code with NotImplementedError
4. **Generate Tests** - Create failing tests for the node
5. **Update State** - Transition node to "prepared"

---

## Step 1: Select Node

### If node-name provided:

Verify the node exists in `arch/ARCH_SUMMARY.md` and has state `planned`.

### If no node-name provided:

Find eligible nodes:

1. Parse `arch/ARCH_SUMMARY.md`
2. Collect nodes where:
   - State == `planned`
   - Readiness condition satisfied (see Step 2)
3. Select any eligible node (non-deterministic)

**Error Handling:**
- If no eligible nodes exist, report: "No eligible nodes for preparation. All nodes may already be prepared/implemented, or architecture decomposition is incomplete. If all nodes are prepared or implemented, run milestone-wrapup to complete the milestone."

---

## Step 2: Verify Eligibility

Confirm the selected node can be prepared:

**Eligibility Rules:**
- State == `planned`
- AND:
  - Node has no children (atomic)
  - OR all children have state == `implemented`

**Hard Refusal Conditions:**
- Selected node has child not `implemented` (if has children)
- Selected node is already `prepared` or `implemented`
- No nodes with state `planned` exist (run `milestone-init` first)

**Error Handling:**
- If node fails eligibility, select another eligible node or report failure

---

## Step 3: Generate Skeleton

Read the node's documentation to understand the contract:

1. First read `arch/nodes/<NodePath>.md` for structural contract (responsibility, input/output)
2. Then read `milestones/{milestone}/nodes/{NodePath}.md` for milestone-specific capabilities

### Check for Existing Implementation

Before generating anything, check if `src/<node_path>.py` already exists:

**If file exists:**
- Read the existing implementation
- Compare with required interface from milestone capabilities
- For each required method that does NOT exist:
  - Add the method with `raise NotImplementedError`
  - Do NOT modify existing methods
- Preserve all existing logic intact

**If file does NOT exist:**
- Generate new skeleton

**Error Handling:**
- If `arch/nodes/<NodePath>.md` does not exist, report: "Node contract undefined. Cannot prepare node without documentation at arch/nodes/<NodePath>.md. Run arch-decompose first to create the node documentation."
- If `milestones/{milestone}/nodes/{NodePath}.md` does not exist, report: "Milestone capabilities undefined. Run milestone-init first to define node capabilities for this milestone."

Generate:

- **File location**: `src/<node_path>.py` (e.g., `auth/UserValidator` → `src/auth/user_validator.py`)
- Module/class definition
- Public interface per contract (functions, methods)
- Data structures
- **All methods raise `NotImplementedError`**

### Strict Prohibitions

- **DO NOT REVERT** existing implementation from past milestones
- No logic implementation for new methods beyond NotImplementedError
- No partial logic
- No wiring code
- No child invocation
- No temporary return values
- No "pass for now"

For existing nodes: add NotImplementedError for NEW methods only.
For new nodes: skeleton must be structurally complete but behaviorally empty.

---

## Step 4: Generate Tests

Read the node's documentation to understand expected behavior.

### Critical: Real Functional Tests vs Structural Tests

**THIS IS THE MOST IMPORTANT PART OF NODE-PREP.**

Tests must define desired behavior — not confirm absence of implementation.

```
✅ CORRECT (functional test):
assert calculate_total([10, 20, 30]) == 60

❌ WRONG (expecting exception):
expect_exception(NotImplementedException)

❌ WRONG (structural test):
assert MyClass is not None
assert my_method is callable
```

### Check for Existing Tests

Before generating tests, check if `tests/<node_path>.py` already exists:

**If test file exists:**
- Read existing tests
- Keep all existing passing tests intact
- Add NEW tests for milestone capabilities that are NOT yet covered
- New tests should FAIL because the new functionality is missing

**If test file does NOT exist:**
- Generate new test file following guidelines below

### Test Generation Guidelines

Generate tests that:

- Target public interface only
- Reflect parent contract
- Cover:
  - Nominal behavior (happy path)
  - Edge cases
  - Failure semantics (verify functions raise appropriate errors like ValueError, TypeError)
  - Invariants
- Express real input/output expectations

### Test Requirements

- **NEW tests** must **fail** (red state) because new behavior is missing
- Tests must **fail** because behavior is wrong, NOT because exceptions are expected
- Do not mock internal children
- Do not inspect internals
- Do not duplicate child testing
- **Keep existing passing tests** - do not modify tests that already pass

### File Path Convention

Place implementation and test files in paths that match the architecture hierarchy.

**Implementation path:**
- Location: `src/<node_path>.py`
- Convert node path to snake_case (e.g., `auth/UserValidator` → `src/auth/user_validator.py`)

**Test path:**
- Location: `tests/<node_path>.py`
- Prefix test file with `test_` (e.g., `tests/auth/test_user_validator.py`)

**Test function naming:**
- `test_<method>_<expected_behavior>`
  - e.g., `test_validate_email_returns_true_for_valid_email`
  - e.g., `test_validate_email_raises_error_for_empty_string`
- **Group by functionality**: Happy path, error handling, edge cases

### Explicitly Forbidden Test Patterns

Do NOT generate any of these:

1. **NotImplementedError-expecting tests** - Tests that assert methods throw NotImplementedError or NotImplementedException
2. **Structural validation tests** - Tests that only check:
   - Object instantiation
   - Method existence
   - Mock wiring behavior
   - Interface shape validation
3. **Integration tests** - Tests spanning multiple nodes or external systems
4. **Passing red-state tests** - Any test that passes when the skeleton is unimplemented

### Red State Definition

After node-prep, the correct state is:

- ✅ All functional tests FAIL (behavior missing)
- ✅ All tests COMPILE (no syntax errors)
- ✅ NO test passes due to expected exceptions
- ✅ NO mock-based structural confirmation tests exist
- ✅ NO integration tests exist

The red state must reflect **missing behavior**, not **intentionally passing failure checks**.

### Composite Node Rule (decomposed nodes)

If node has children:

- Tests validate orchestration behavior only
- Children are assumed correct
- Do not re-verify child functionality

---

## Step 5: Update State

In `arch/ARCH_SUMMARY.md`, change the node's status:

```
atomic → prepared
decomposed → prepared
```

No other transitions allowed in this skill.

---

## Constraints

### Explicit Prohibitions

The skill must NOT:

- Write tests expecting `NotImplementedError` or `NotImplementedException`
- Write "tests that pass in red" (exception is expected, so test passes)
- Write mock-only structure validation tests
- Write integration tests
- Validate stub runtime failure

### What This Skill Does NOT Do

- Choose milestone priority
- Enforce strict ordering
- Implement logic
- Modify architecture structure
- Expand subtree
- Modify node contracts (that's milestone-init's job)
- Move nodes to "implemented" (that's node-build's job)

---

## Parallelism Model

This system permits:

- Multiple `prepared` nodes simultaneously
- Independent bottom-up progress
- Parallel implementation tasks

The only structural invariant:

> A node may only move to `implemented` after all children are `implemented`.

That invariant preserves correctness even under parallel prep.

---

## Global Invariants

Must always hold:

1. No node implemented before its children
2. No node prepared before its children are implemented (if decomposed)
3. All nodes are part of architecture
4. Tests must exist before implementation
5. Architecture is immutable during implementation phase

---

## Success Criteria

- [ ] Node selected (provided or auto-detected)
- [ ] Eligibility verified
- [ ] Existing implementation preserved (not reverted)
- [ ] Skeleton generated for new methods (NotImplementedError for new methods only)
- [ ] New failing tests generated for new capabilities
- [ ] Existing passing tests kept intact
- [ ] Node state updated to "prepared"
- [ ] No logic implemented for new methods beyond NotImplementedError

## Next Steps

After preparing this node:

- **Implement logic**: Run `node-build` for this node to move it to "implemented"
- **Add tests for modified**: Run `milestone-test-add` when all nodes are implemented
