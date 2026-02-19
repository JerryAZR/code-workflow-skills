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

<HARD-GATE>
Do NOT write tests that expect NotImplementedException. Tests must define expected behavior, not confirm absence of implementation.
</HARD-GATE>

<HARD-GATE>
Do NOT allow any test to pass in red state. Red state must occur because behavior is missing, not because throwing is expected.
</HARD-GATE>

## Workflow

Follow this process in order:

1. **Locate target node** - Find the node in ARCH_SUMMARY.md and its documentation
2. **Define structural skeleton** - Create class/module with method signatures, all raising NotImplementedError
3. **Define child interfaces** - Create abstract/interface definitions for immediate children
4. **Write unit tests** - Create tests for current node's expected behavior
5. **Generate interface assertions** - Define contracts for child nodes
6. **Create child node documentation** - Create docs for each immediate child in nodes/ subfolder
7. **Update current node documentation** - Record structural definitions, tests, and contracts
8. **Verify test structure** - Ensure tests compile and fail as expected

## Step 1: Locate Target Node

Find the target node in the architecture:

1. Read `arch/ARCH_SUMMARY.md` to locate the node in the tree hierarchy
2. Read the node's documentation at `arch/nodes/<NodeName>.md` (or `arch/<RootNodeName>.md` for root node)
3. Identify the node's immediate children (first-level only)

If the user provided a node name, match it against the ARCH_SUMMARY.md hierarchy.

## Step 2: Define Structural Skeleton

Create the structural skeleton for the current node **before writing any tests**:

### Structural Skeleton Requirements

1. **Create the class/module** with the public interface from node docs
2. **Define public method signatures** matching the documented APIs
3. **Implement constructor** with dependency injection points for child nodes
4. **Raise NotImplementedError** (or equivalent) in every public method
5. **No fake return values** - methods must raise exceptions, not return placeholders

### Implementation Pattern

```python
# Example (Python)
class NodeClass:
    def __init__(self, child_node: ChildInterface):
        self._child = child_node  # Dependency injection

    def public_method(self, param: Type) -> ReturnType:
        raise NotImplementedError("Behavior not implemented")

    def another_method(self) -> ReturnType:
        raise NotImplementedError("Behavior not implemented")
```

### Language-Specific Notes

- **Python**: Use `raise NotImplementedError("...")`
- **TypeScript/JavaScript**: Use `throw new Error("...")`
- **Java**: Use `throw new UnsupportedOperationException("...")`
- **Go**: Use `panic("not implemented")` or return zero values with error
- **Rust**: Use `unimplemented!()` or `panic!("not implemented")`

**CRITICAL**: Do NOT return dummy values, None (unless documented), or fake data. The system must be in intentional red state.

## Step 3: Define Child Interfaces

Create abstract/interface definitions for **immediate children only** (first-level subnodes):

### Interface Requirements

1. **Define interface types** - Abstract classes or interface definitions
2. **Declare method signatures** - Match the contracts from child node docs
3. **No implementation** - Only type definitions, no behavioral code
4. **Mark as stub** - Interface exists but has no working implementation

### What to Include

- Input parameter types
- Output return types
- Exception types that may be raised

### What NOT to Include

- No implementation logic
- No stub behavior
- No wiring to other components
- No parent node awareness

```python
# Example - Child Interface (Python)
from abc import ABC, abstractmethod

class ChildInterface(ABC):
    @abstractmethod
    def process(self, data: InputType) -> OutputType:
        pass

    @abstractmethod
    def validate(self, item: ItemType) -> bool:
        pass
```

## Step 4: Write Unit Tests

Write full unit tests for the current node's expected behavior:

### !!! CRITICAL: What NOT to Write

**NEVER write tests that:**

- Assert methods throw `NotImplementedException` or similar
- Validate stub failure behavior
- Pass in the unimplemented state
- Only check object instantiation or method existence
- Use mocks to confirm skeleton structure

These are **false-green tests** that break TDD discipline.

### What TO Write

**Write real functional unit tests that:**

- Define expected behavior of the current node
- Cover happy paths and edge cases
- Express real input/output expectations
- Test behavior through abstract child interfaces (using mock/stub implementations)

Example (correct pattern):
```python
def test_process_valid_input_returns_result():
    result = node.process(valid_input)
    assert result.success == True
    assert result.data == expected_output
```

NOT:
```python
def test_process_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        node.process(any_input)
```

### Test Coverage Requirements

Tests must cover:
- **Functional logic** - Core behavior described in responsibility
- **Edge cases** - Boundary conditions, error states, invalid inputs
- **Child node interactions** - Calls to child nodes through their contracts

### Red Discipline

- Tests must **fail initially** because behavior is missing, NOT because exceptions are expected
- Use descriptive test names that explain expected behavior
- Include assertions that verify outputs match contracts
- Document expected failures for unimplemented code

## Step 5: Generate Interface Assertions

Define assertions that verify child nodes conform to their contracts:

### What to Assert

- **Inputs to child nodes** - Parameters passed match expected types/shapes
- **Outputs from child nodes** - Return values match expected contracts
- **Call patterns** - Correct methods called with correct arguments

### What NOT to Do

- Do NOT implement child nodes
- Do NOT write internal logic for stubs
- Do NOT write tests that verify stub runtime failure
- Do NOT write mock-only structure validation tests (object instantiation, method existence)
- Only check inputs/outputs at the interface level through functional tests

## Step 6: Create Child Node Documentation

Create documentation for each immediate child node:

### Documentation Structure

1. Create a folder named `nodes/` in the same directory as the current node's doc
2. For each child node, create `nodes/<ChildNodeName>.md`

### Child Node Documentation Content

Document only what's known from contracts and interfaces:

```markdown
# <ChildNodeName>

## Status

stub

## Interface Contract

### Exposed APIs
- `methodName(param: Type): ReturnType` - <Brief purpose>

### Expected Input Shape
- <Parameter descriptions>

### Expected Output Shape
- <Return value descriptions>

## Parent Expectations

### How Parent Will Use This Node
- <What methods parent is expected to call>

### Contract with Parent
- Input requirements
- Output guarantees
```

### What NOT to Include

- No implementation guidance
- No algorithm descriptions
- No internal structure details
- No behavioral specifications beyond contracts

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

## Step 8: Verify Test Structure

Run the full test suite to verify tests work correctly:

1. **Execute tests** - Run the full test suite for the node
2. **Verify failures** - Tests MUST fail (node is unimplemented)
3. **Check error messages** - Failures should clearly indicate what's missing
4. **Detect false-green** - Ensure no tests pass due to expected exceptions
5. **Fix broken tests** - If tests pass or error unexpectedly, fix the test

### False-Green Detection Checklist

After running tests, verify:

- [ ] No tests pass because they expect NotImplementedException
- [ ] No tests pass due to object instantiation checks
- [ ] No tests pass due to mock wiring verifications
- [ ] All failures are due to missing behavior (AttributeError, TypeError, AssertionError)
- [ ] Tests compile without errors

If tests pass unexpectedly, either:
- The node is already implemented (verify status in node docs)
- The test is faulty and cannot detect missing implementation (fix the test)
- The test is a false-green test (remove it and write real functional test)

## Constraints

### Explicit Prohibitions

The skill must NOT write:

- Tests expecting `NotImplementedException` or similar
- Tests that pass in red state
- Mock-only structure validation tests
- Integration tests
- Tests validating stub runtime failure
- Tests checking only object instantiation or method existence

### What This Skill Does NOT Do

- Implement behavioral logic - only structural skeleton with NotImplementedError
- Return placeholder values or fake data
- Wire implementations together
- Reference parent nodes beyond defined contracts
- Recursively decompose beyond immediate children
- Test above the current node (parents) or below (grandchildren)
- Write stub behavior in child interfaces

## Success Criteria

- [ ] Target node located in ARCH_SUMMARY.md hierarchy
- [ ] Node documentation read and contracts extracted
- [ ] Structural skeleton created (class/module with NotImplementedError)
- [ ] Child interfaces defined (abstract/interface types only)
- [ ] Unit tests written for current node's responsibility
- [ ] Real functional tests (NOT exception-expecting tests)
- [ ] Edge cases covered in tests
- [ ] Interface assertions defined for each child node
- [ ] Node documentation updated with structural definitions, tests, and contracts
- [ ] Tests compile successfully
- [ ] Tests fail as expected (red discipline - due to missing behavior, NOT expected exceptions)
- [ ] No false-green tests exist
- [ ] Only current node and immediate children affected

### Correct Red State Definition

After node-prep:

- Structural skeleton exists (methods raise NotImplementedError)
- Interfaces are declared
- Real behavioral unit tests exist
- All functional tests fail because behavior is missing
- No tests pass due to expected exceptions
- No mock-only structural confirmation tests exist

The red state must reflect missing behavior, not intentionally passing failure checks.

## Next Steps

After node-prep execution:

- **Tests fail due to missing behavior** - Tests define the contract; proceed to implement the node using `node-build` skill
- **Tests pass unexpectedly** - Likely a false-green test; fix by writing real functional test
- **Tests fail due to NotImplementedException** - This is wrong; fix by writing tests that define expected behavior
- **To implement node** - Invoke `node-build` skill to write the implementation
