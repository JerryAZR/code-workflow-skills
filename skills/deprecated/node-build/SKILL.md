---
name: node-build
description: "[DEPRECATED] Top-down TDD node implementation. Use bottom-up implementation instead - see skill workflow documentation."
argument-hint: "[node-name or node-path]"
---

# Node Build (DEPRECATED)

## ⚠️ DEPRECATED

**This skill is deprecated because it assumes a top-down implementation flow which does not work well with LLMs.**

The top-down approach (root → children) creates problems:
- LLMs lose context when implementing deep trees
- Child nodes can't be properly tested until parents exist
- Forward references are fragile

**Use bottom-up implementation instead:** Start with leaf nodes and work upward.

## Overview

Move the current node from red to green by implementing full functional logic, complete wiring/glue logic, and minimal child stubs with contract-compliant behavior. This skill implements only the current node and its immediate child stubs—it must not expand architecture or recurse into child implementations.

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides an argument (e.g., a node name or path), treat it as the target node. Try to satisfy the request directly. If the request seems unclear or suboptimal, clearly argue against it with alternatives. If the user has settled on a decision, respect it and make it work.

## Prerequisites

Before invoking this skill, ensure:

1. **Node structure exists** - Class/module with method signatures defined (via node-prep)
2. **Child interfaces are defined** - Abstract/interface definitions for immediate children
3. **Unit tests exist** - Tests and interface assertions defined (via node-prep)
4. **Project compiles** - No syntax errors in test files
5. **Tests are in red state** - Tests fail due to NotImplementedError

## Hard Gates

<HARD-GATE>
Do NOT proceed if any prerequisite is missing. Stop and invoke the appropriate skill first (node-prep).
</HARD-GATE>

<HARD-GATE>
Do NOT expand architecture or recurse into child implementations. This skill implements only the current node.
</HARD-GATE>

<HARD-GATE>
Do NOT waive tests or skip failing assertions. Tests must pass through proper implementation.
</HARD-GATE>

## Workflow

Follow this process in order:

1. **Validate preconditions** - Verify all prerequisites are met
2. **Analyze tests** - Understand what behavior each test validates
3. **Implement current node** - Write full functional logic
4. **Implement child stubs** - Create minimal contract-compliant behavior
5. **Run tests** - Verify all tests pass
6. **Verify constraints** - Ensure no scope leakage

## Step 1: Validate Preconditions

Verify all prerequisites exist before proceeding:

1. Check that node structure exists (class/module with method signatures)
2. Verify child interfaces are defined (abstract classes/interfaces)
3. Confirm unit tests and assertions exist
4. Ensure project compiles without syntax errors
5. Verify tests fail due to NotImplementedError (red state)

If any precondition fails, abort and invoke `node-prep` first.

## Step 2: Analyze Tests

Understand the test suite before implementing:

1. Read each test to understand what behavior it validates
2. Identify tests that validate parent behavior vs child behavior
3. Flag tests that depend on sophisticated child logic
4. Determine minimal child stub behavior needed

## Step 3: Implement Current Node

Implement the full functional logic of the current node:

### Implementation Requirements

1. **Implement all public methods** - Complete the skeleton with real logic
2. **Complete wiring/orchestration** - Connect child nodes properly
3. **Satisfy all unit tests** - Make all tests pass
4. **Cover edge cases** - Handle all cases already defined in tests
5. **No speculative features** - Implement only what tests require

### Red Discipline

- Start from red state (tests failing)
- Write implementation to make tests pass
- Do not modify tests to make them pass
- Do not return placeholder values

## Step 4: Implement Child Stubs

Implement minimal stubs for immediate child nodes:

### Stub Requirements

1. **Minimal deterministic behavior** - Return valid contract-compliant values
2. **Contract-compliant** - Satisfy interface contracts
3. **Only what's needed** - Implement only the minimal logic for parent tests to pass
4. **NOT real business logic** - Stubs are placeholders, not implementations
5. **NOT expanded** - Do not add responsibilities beyond contracts

### Stub Pattern

```python
# Example - Minimal Child Stub (Python)
class ChildStub(ChildInterface):
    def process(self, data: InputType) -> OutputType:
        # Minimal deterministic return that satisfies contract
        return OutputType(success=True, data=data.value)

    def validate(self, item: ItemType) -> bool:
        # Always return True - minimal stub
        # Real validation deferred to child implementation
        return True
```

### Key Principle

Child stubs are collaborators, not partial implementations. They exist to satisfy parent tests, not to provide real functionality.

## Step 5: Handle Tests Requiring Sophisticated Child Logic

If a unit test cannot pass without implementing real child logic:

### Analysis Required

1. **Do NOT waive the test** - Tests define contracts
2. **Do NOT implement full child behavior** - This expands scope
3. **Analyze the test scope** - Is this testing parent or child?

### Resolution Options

1. **Refactor the test** - Isolate parent behavior independently of child correctness
2. **Use deterministic stub** - Return predictable values that allow parent logic to be tested
3. **Reclassify** - If test inherently validates child correctness, mark as integration test

### Example Resolution

```python
# Before: Test expects child to filter valid items
def test_process_filters_invalid_items():
    result = parent.process(items)
    # This test validates child behavior, not parent
    assert result == [valid_item]  # Requires child to filter

# After: Refactor to test parent behavior only
def test_process_passes_all_items_to_child():
    # Test that parent calls child with all items
    parent.process(items)
    child.process.assert_called_with(items)  # Parent behavior verified
```

## Step 6: Run Tests

Execute the full test suite to verify implementation:

1. **Run all tests** - Execute complete test suite
2. **Verify all pass** - Every test must pass
3. **Check error messages** - No unexpected errors
4. **Confirm green state** - All tests passing

If tests fail:
- Review implementation against test expectations
- Adjust child stubs if needed
- Do NOT modify tests to make them pass

## Step 7: Verify Constraints

Ensure no scope leakage occurred:

1. **No architecture changes** - Did not modify arch documents
2. **No new tests** - Did not generate new test cases
3. **No relaxed contracts** - Interface contracts unchanged
4. **No child recursion** - Did not implement beyond stubs
5. **No optimization** - No code beyond what tests require

## Constraints

### What This Skill Does NOT Do

- Modify architecture documents (arch/ARCH_SUMMARY.md, arch/nodes/)
- Generate new tests (only minimal corrections if structurally invalid)
- Relax interface contracts
- Recurse into child node implementations
- Optimize beyond test requirements
- Introduce parent-awareness logic in children

### What Child Stubs Are NOT

- Partial implementations
- Real business logic
- Expanded responsibilities
- Full-featured components

## Success Criteria

- [ ] All unit tests pass
- [ ] All interface assertions pass
- [ ] Child stubs are minimal and contract-compliant
- [ ] No sophisticated child logic introduced
- [ ] Parent behavior fully implemented
- [ ] No scope leakage (no architecture changes)
- [ ] Tests in green state

## Next Steps

After node-build execution:

- **Tests pass** - Node implementation complete
- **To prepare next node** - Invoke `node-prep` for the next node
- **To build child** - When ready, invoke `node-build` for child nodes

---

## Reference: Child Stub Patterns by Language

### Python

```python
class ChildStub(ChildInterface):
    def method(self, param: Type) -> ReturnType:
        # Return minimal valid value
        return ReturnType(field=value)
```

### TypeScript/JavaScript

```typescript
class ChildStub implements ChildInterface {
  method(param: Type): ReturnType {
    // Return minimal valid value
    return { field: value };
  }
}
```

### Java

```java
public class ChildStub implements ChildInterface {
    @Override
    public ReturnType method(Type param) {
        // Return minimal valid value
        return new ReturnType(value);
    }
}
```

### Go

```go
type ChildStub struct{}

func (s *ChildStub) Method(param Type) ReturnType {
    // Return minimal valid value
    return ReturnType{Field: value}
}
```

### Rust

```rust
struct ChildStub;

impl ChildInterface for ChildStub {
    fn method(&self, param: Type) -> ReturnType {
        // Return minimal valid value
        ReturnType { field: value }
    }
}
```
