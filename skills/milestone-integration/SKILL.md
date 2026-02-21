---
name: milestone-integration
description: "Creates integration and end-to-end tests that verify all milestone features work together. Use when all nodes are implemented and ready for milestone wrapup, to provide confidence before manual verification."
argument-hint: "[milestone-name]"
---

# Milestone Integration

## Overview

Create integration and end-to-end (E2E) tests that verify the features listed in the manual verification checklist work together correctly. This provides automated confidence before presenting to the user for manual verification.

This skill bridges the gap between unit tests (per-node) and manual verification:
- **Unit tests** verify individual node behavior (handled by node-prep/node-build)
- **Integration tests** verify nodes work together (this skill)
- **Manual verification** verifies user-observable behavior (milestone-wrapup)

**User's Intent:** $ARGUMENTS

## Prerequisites

- `milestones/{index}-{name}/capabilities.md` exists with manual verification checklist
- All nodes for the milestone have state `implemented`
- Node implementations exist at `src/<node_path>.py`
- Unit tests exist at `tests/<node_path>.py`

## Workflow

Follow this process in order:

1. **Read Capabilities** - Extract features to verify from capabilities.md
2. **Identify Integration Points** - Determine how nodes interact
3. **Generate Integration Tests** - Create tests that verify feature combinations
4. **Run Tests** - Verify integration tests pass
5. **Fix Issues** - If tests fail, diagnose and fix

---

## Step 1: Read Capabilities

Read `milestones/{index}-{name}/capabilities.md` to extract:

1. **Manual Verification Checklist** - The features listed under "Features to Verify"
2. **How to Start** - The startup command for the application

### Extract Features

From the "Features to Verify" section, list each feature that needs integration testing:

```
- Feature 1
- Feature 2
...
```

---

## Step 2: Identify Integration Points

Analyze the architecture to understand how features interact:

1. Read `arch/ARCH_SUMMARY.md` to understand node relationships
2. Identify which nodes participate in each feature
3. Determine the data flow between nodes for each feature

### Common Integration Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Chained Processing** | Output of one node becomes input of another | Parser → Validator → Formatter |
| **Aggregated Results** | Multiple nodes contribute to final output | Metrics + Aggregator → Report |
| **Sequential Operations** | Nodes called in sequence | Load → Process → Save |
| **Shared State** | Nodes share data through common context | Config → Multiple Workers |

---

## Step 3: Generate Integration Tests

Create integration tests that verify features work together.

### Test File Location

**Integration tests directory:** `tests/integration/`

**File naming:** `tests/integration/test_{milestone_name}.py`

Example: For milestone "1-core-skeleton" → `tests/integration/test_core_skeleton.py`

### Test Structure

```python
import pytest

class TestMilestoneIntegration:
    """Integration tests for milestone features."""

    def test_feature_name_integration(self):
        """Verify feature works end-to-end."""
        # Set up any required fixtures
        # Execute the feature through the full stack
        # Verify the expected outcome
        pass
```

### Test Requirements

Generate tests that:

- **Exercise the full feature** - Start from public API, go through nodes, produce result
- **Verify actual behavior** - Not mocked, not stubbed
- **Cover happy path** - Main user scenarios work
- **Include setup/teardown** - Clean state between tests

### Integration vs Unit Tests

| Aspect | Unit Tests | Integration Tests |
|--------|------------|------------------|
| Scope | Single node | Multiple nodes |
| Mocks | Allowed | Minimal/None |
| External deps | Mocked | Real or integrated |
| Speed | Fast | Slower |

### Explicitly Forbidden Patterns

Do NOT generate:

1. **Re-unit-test** - Don't re-test individual node logic (that's in unit tests)
2. **Full system tests** - Don't test external services, databases, APIs
3. **UI interaction tests** - Don't test clicks, renders (that's E2E/manual)

---

## Step 4: Run Tests

Execute the integration tests:

```bash
pytest tests/integration/ -v
```

**Expected Result:** All integration tests PASS

If tests fail, proceed to Step 5.

---

## Step 5: Fix Issues

If integration tests FAIL:

1. **Analyze failure**: Is it a unit test issue or integration issue?
2. **If unit test issue**: The node's unit tests need fixing (use node-test-add or node-build)
3. **If integration issue**: Fix the integration/wiring between nodes

**Common integration issues:**
- Missing method calls between nodes
- Incorrect parameter passing
- Missing initialization/setup
- State not properly passed between nodes

Fix and re-run until tests pass.

---

## Constraints

### What This Skill Does

- Creates integration tests for milestone features
- Verifies nodes work together correctly
- Provides automated confidence before manual verification

### What This Skill Does NOT Do

- Modify node implementations (except trivial fixes)
- Create unit tests (that's node-prep/node-build/node-test-add)
- Perform manual verification (that's milestone-wrapup)
- Test external systems or databases

---

## Success Criteria

- [ ] Features extracted from capabilities.md
- [ ] Integration points identified
- [ ] Integration tests generated
- [ ] Tests pass (all features work together)

## Next Steps

After integration tests pass:
- **Manual verification**: Run `milestone-wrapup` to present checklist to user
- **If issues found**: Fix and re-run integration tests
