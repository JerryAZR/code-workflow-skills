---
name: node-build
description: "Implements a prepared node to make tests pass and transition the node to implemented. Use when a node with state 'prepared' is ready for implementation."
argument-hint: "[node-name]"
---

# Node Build

## Overview

Implement one prepared node so that tests pass, architecture remains coherent, and the node transitions to "implemented".

This skill follows a bottom-up approach with TDD discipline.

**User's Intent:** $ARGUMENTS

If no node-name provided, find an eligible prepared node automatically.

## Prerequisites

- `arch/ARCH_SUMMARY.md` exists with prepared nodes
- Node has state "prepared"
- Tests exist and fail (from node-prep)
- Run node-prep first to prepare a node

## Node State Model

| State | Meaning |
|-------|---------|
| `atomic` | Leaf node scheduled for this milestone |
| `decomposed` | Non-leaf node scheduled for this milestone |
| `prepared` | Skeleton + failing tests created |
| `implemented` | Logic implemented and tests passing |

## Workflow

Follow this process in order:

1. **Select Target** - Find eligible prepared node
2. **Pre-Checks** - Confirm tests exist and fail, interface matches
3. **Implement** - Write minimal logic to pass tests
4. **Handle Missing Data** - Extend child interfaces if needed
5. **Verify** - Confirm all tests pass
6. **Update State** - Transition to "implemented"

---

## Step 1: Select Target

### If node-name provided:

Verify the node exists in `arch/ARCH_SUMMARY.md` and has state "prepared".

### If no node-name provided:

Find eligible nodes:

1. Parse `arch/ARCH_SUMMARY.md`
2. Collect nodes where state == "prepared"
3. Select any eligible node (non-deterministic)

**Refuse if:**
- No prepared node exists
- Any child is not "implemented"

**Error Handling:**
- If no eligible nodes exist, report: "No eligible nodes for building. Run node-prep first to prepare a node. If all nodes are already implemented, run milestone-wrapup to complete the milestone."

---

## Step 2: Pre-Checks

Before coding, confirm:

1. **Tests exist and fail** - Run tests to confirm red state
   - Tests location: `tests/<node_path>.py` (e.g., `tests/auth/test_user_validator.py`)
2. **Public interface matches architecture** - Verify class/method signatures match contract
   - Implementation location: `src/<node_path>.py`
3. **No logic already present** - Confirm methods still raise NotImplementedError

**Refuse if tests already pass** - Return to user, something is wrong.

---

## Step 3: Implement

Implement minimal logic required to pass tests.

### Strict Constraints

- Do NOT change public interface (unless extension required)
- Do NOT change tests (unless incorrect)
- Do NOT modify siblings
- Do NOT re-decompose

### Atomic Node

- Implement internal behavior only
- No child orchestration needed

### Decomposed Node

- Orchestrate children only
- Do not duplicate child logic
- Use child public interfaces only

---

## Step 4: Handle Missing Data

### Case A — Missing Parent Data

Allowed:

1. Extend current node input interface explicitly
2. Update architecture contract
3. Continue

Parent will satisfy later.

### Case B — Missing Child Data

Allowed (additive only):

1. Extend child public interface
2. Patch child implementation
3. Mark child: `implemented → modified`
4. Log:
   - What was added
   - Why
   - Which parent required it

**Constraints:**
- Must be additive
- Existing tests must remain green

---

## Step 5: Verify

All tests must pass.

**If failure:**
- Fix implementation
- If interface updated, fixing tests to use the new interface is allowed
- Do not weaken tests

---

## Step 6: Update State

In `arch/ARCH_SUMMARY.md`, change the node's status:

```
prepared → implemented
```

If child extension occurred:

```
child: implemented → modified
parent: prepared → implemented
```

No other transitions allowed in this skill.

---

## Constraints

### What This Skill Does NOT Do

- Choose milestone priority
- Prepare nodes (that's node-prep's job)
- Decompose nodes (that's node-decompose's job)
- Modify architecture structure (except minimal child extensions)
- Weaken tests to make them pass

---

## Global Invariants

Must always hold:

1. No node implemented before children
2. Child modification must be additive
3. Existing passing tests must remain passing
4. No silent contract mutation
5. Architecture document updated when interface changes

---

## Success Criteria

- [ ] Node selected (provided or auto-detected)
- [ ] Pre-checks passed (tests fail, interface matches)
- [ ] Minimal implementation added
- [ ] All tests pass
- [ ] Node state updated to "implemented" (or "modified" if child extended)
- [ ] No public interface changed (unless required)
- [ ] No tests weakened

## Next Steps

After building:

- **Prepare more**: Run `node-prep` to prepare more nodes
- **Continue building**: Run `node-build` for another prepared node
- **Wrap up milestone**: Run `milestone-wrapup` when all nodes are implemented
