---
name: node-prep
description: "Prepares architecture nodes for implementation by writing unit tests and interface assertions. Use when an architecture node is ready to be implemented and needs test contracts defined."
argument-hint: "[node-name or node-path]"
---

# Node Preparation

## Overview

Prepare the current architecture node for implementation by generating unit tests and interface assertions that enforce contracts with child nodes. This skill focuses strictly on the current node and its immediate subnodes—no work is done above or below this boundary.

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides an argument (e.g., a node name or path), treat it as the target node. Try to satisfy the request directly. If the request seems unclear or suboptimal, clearly argue against it with alternatives. If the user has settled on a decision, respect it and make it work.

## Prerequisites

Before invoking this skill, ensure:

1. **Architecture exists** - `arch/ARCH_SUMMARY.md` must exist with the node hierarchy (invoke `root-architect`)
2. **Node documentation exists** - The target node must have a documentation file at `arch/nodes/<NodeName>.md` (or `arch/<RootNodeName>.md` for root node)
3. **Tech stack is chosen** - The project must have a documented tech stack in SPEC.md (invoke `bootstrap`)
4. **Node status is stub** - The node must be in "stub" status, meaning it needs implementation

## Hard Gates

<HARD-GATE>
Do NOT proceed if any prerequisite is missing. Stop and invoke the appropriate skill to satisfy the prerequisite first.
</HARD-GATE>

<HARD-GATE>
Do NOT implement the node itself—this skill only writes tests and assertions. Implementation is a separate step.
</HARD-GATE>

<HARD-GATE>
Do NOT work on parent nodes, sibling nodes, or grandchildren. This skill operates only on the current node and its immediate children.
</HARD-GATE>

## Workflow

Follow this process in order:

1. **Locate target node** - Find the node in ARCH_SUMMARY.md and its documentation
2. **Analyze node contract** - Review responsibility, dataflow, and public interface from node docs
3. **Write unit tests** - Create tests for current node's expected behavior
4. **Generate interface assertions** - Define contracts for child nodes
5. **Update node documentation** - Record test coverage and contract definitions
6. **Verify test structure** - Ensure tests compile and follow project conventions

## Step 1: Locate Target Node

Find the target node in the architecture:

1. Read `arch/ARCH_SUMMARY.md` to locate the node in the tree hierarchy
2. Read the node's documentation at `arch/nodes/<NodeName>.md` (or `arch/<RootNodeName>.md` for root node)
3. Identify the node's immediate children (first-level only)

If the user provided a node name, match it against the ARCH_SUMMARY.md hierarchy.

## Step 2: Analyze Node Contract

Review the node documentation to understand:

- **Responsibility** - What the node owns and is accountable for
- **Dataflow** - Inputs, outputs, and side-effects
- **Public Interface** - Exposed APIs, events, and configuration
- **Dependencies** - What the node requires from child nodes
- **Invariants** - Statements that must always hold

Extract the key contracts that tests must verify.

## Step 3: Write Unit Tests

Write full unit tests for the current node's expected behavior:

### Test Coverage Requirements

Tests must cover:
- **Functional logic** - Core behavior described in responsibility
- **Edge cases** - Boundary conditions, error states, invalid inputs
- **Child node interactions** - Calls to child nodes through their contracts

### Red Discipline

- Tests must **fail initially** if the node is unimplemented
- Use descriptive test names that explain expected behavior
- Include assertions that verify outputs match contracts
- Document expected failures for unimplemented code

## Step 4: Generate Interface Assertions

Define assertions that verify child nodes conform to their contracts:

### What to Assert

- **Inputs to child nodes** - Parameters passed match expected types/shapes
- **Outputs from child nodes** - Return values match expected contracts
- **Call patterns** - Correct methods called with correct arguments

### What NOT to Do

- Do NOT implement child nodes
- Do NOT write internal logic for stubs
- Do NOT verify edge-case behavior inside stubs
- Only check inputs/outputs at the interface level

## Step 5: Update Node Documentation

Record all test cases and interface assertions in the node documentation:

1. Open `arch/nodes/<NodeName>.md` (or `arch/<RootNodeName>.md` for root node)
2. Add a **Test Coverage** section documenting:
   - What each test verifies
   - Which contracts are enforced
   - Which child nodes are stubbed (not implemented)
3. Update the **Status** from "stub" to "partial" if tests are defined

```markdown
## Test Coverage

### Unit Tests

Document all test cases using industrial naming conventions:
- `test_<method>_<expected_behavior>` - e.g., `test_process_valid_input_returns_result`
- Group by functionality (happy path, error handling, edge cases)

### Interface Assertions

Document contracts for each child node:
- Input contract: expected parameter types/shapes
- Output contract: expected return types/shapes
- Mark child nodes as stubbed if unimplemented

### Coverage Notes

List what is NOT covered by tests (defer to implementation phase)
```

## Step 6: Verify Test Structure

Run the full test suite to verify tests work correctly:

1. **Execute tests** - Run the full test suite for the node
2. **Verify failures** - Tests MUST fail (node is unimplemented)
3. **Check error messages** - Failures should clearly indicate what's missing
4. **Fix broken tests** - If tests pass or error unexpectedly, fix the test

If tests pass unexpectedly, either:
- The node is already implemented (verify status in node docs)
- The test is faulty and cannot detect missing implementation (fix the test)

## Constraints

### What This Skill Does NOT Do

- Implement the node or child nodes
- Write stubs or placeholder code
- Wire components together
- Reference parent nodes beyond defined contracts
- Verify full functional behavior of child nodes
- Test above the current node (parents) or below (grandchildren)

## Success Criteria

- [ ] Target node located in ARCH_SUMMARY.md hierarchy
- [ ] Node documentation read and contracts extracted
- [ ] Unit tests written for current node's responsibility
- [ ] Edge cases covered in tests
- [ ] Interface assertions defined for each child node
- [ ] Node documentation updated with test coverage
- [ ] Tests follow project conventions and compile
- [ ] Only current node and immediate children affected

## Next Steps

After node-prep execution:

- **Tests fail (expected)** - Tests define the contract; proceed to implement the node using `node-build` skill
- **Tests pass unexpectedly** - Test may be faulty; fix the test to properly detect unimplemented code
- **To implement node** - Invoke `node-build` skill to write the implementation
