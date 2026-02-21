---
name: milestone-wrapup
description: "Concludes the current milestone by verifying implementation progress and documenting achievements. Use when a milestone's work is complete and ready for review. The next milestone will be started separately via milestone-init."
argument-hint: "[milestone-number]"
---

# Milestone Wrap-up

## Overview

Verify that the current milestone is complete and document what has been achieved.

**User's Intent:** $ARGUMENTS

This skill concludes milestone completion with proper verification and documentation. The next milestone is started separately using milestone-init.

## Prerequisites

- `milestones/MILESTONES.md` exists with milestone definitions
- `arch/ARCH_SUMMARY.md` exists with node states (if architecture exists)

## Workflow

Follow this process in order:

1. **Read Milestone Plan** - Identify current milestone and its scope
2. **Review Architecture Progress** - Check node states in ARCH_SUMMARY.md
3. **Verify Deliverables** - Confirm runnable product or usable library exists
4. **Validate Completeness** - Ensure all required work is done
5. **Manual Verification** - Present checklist for user to verify features (REQUIRED)
6. **Document Achievements** - Record completed work in milestones/MILESTONES.md (only after validation passes)

---

## Step 1: Read Milestone Plan

Read `milestones/MILESTONES.md` to understand:

1. **Current milestone** - Which milestone is in-progress (or specified)
2. **Milestone scope** - What features are included
3. **Success criteria** - What must be complete to wrap up

If no milestone number provided, find the in-progress milestone (status: "in-progress").

**Error Handling:**
- If `milestones/MILESTONES.md` does not exist, report: "No milestone plan found. Create one using milestone-plan-all skill first."
- If no in-progress milestone exists, report: "No milestone is currently in-progress. Use milestone-init to activate a milestone."

---

## Step 2: Review Architecture Progress

If `arch/ARCH_SUMMARY.md` exists, read it to understand implementation progress.

### Check Node States

For each node relevant to the current milestone, verify the state:

| State | Meaning | Acceptable for Wrap-up |
|-------|---------|------------------------|
| `implemented` | Completed and tested | Yes |
| `prepared` | Skeleton ready with failing tests | **No** - needs implementation |
| `atomic` | Not yet started | **No** - needs work |
| `decomposed` | Not yet decomposed | **No** - needs work |

---

## Step 3: Verify Deliverables

### Check for Runnable Product

Depending on the project type, verify one of:

**For applications (web, desktop, CLI):**
- Application can be started (check for entry point)
- No critical runtime errors on startup

**For libraries:**
- Library can be imported/required
- Public API is accessible

**For APIs:**
- Server can start
- Basic endpoints respond

### Run Verification

Execute verification based on project type:

| Type | Command |
|------|---------|
| Library | `python -c "import src"` or `node -e "require('./src')"` |
| CLI | `<command> --help` |
| GUI | Run built executable |

**Error Handling:**
- If no runnable product exists, report: "No runnable product found. Complete implementation before wrap-up."

---

## Step 4a: Self-Check

Perform final checks before marking milestone complete:

### Checklist

- [ ] All required nodes are in acceptable states
- [ ] Runnable product exists and works
- [ ] Milestone scope is fulfilled
- [ ] No critical blockers remain
- [ ] Integration tests exist at `tests/integration/test_{milestone_name}.py`
- [ ] Integration tests cover features listed in `milestones/{index}-{name}/capabilities.md`

### Integration Test Validation

Check if integration tests exist and cover the declared features:

1. Read `milestones/{index}-{name}/capabilities.md` to get the list of features to verify
2. Check if `tests/integration/test_{milestone_name}.py` exists
3. If integration tests don't exist or don't cover all features:
   - Invoke `milestone-integrate` to create them
   - After integration tests are created, re-run this self-check

### Handling Incomplete Work

**If incomplete due to blockers:**
- Do NOT proceed to documentation
- Report what is missing
- Suggest: Continue implementation or adjust milestone scope

**If intentionally incomplete (scope adjustment):**
- May proceed with wrap-up if scope was adjusted

---

## Step 4c: Manual Verification

Present the user with the manual verification checklist from `milestones/{index}-{name}/capabilities.md`.

**If user wants to skip:** Respect their choice and proceed to Step 5.

Wait for user to complete verification before proceeding.

**If user reports issues:**
- Do NOT proceed to document achievements
- Report what needs fixing
- Suggest: Continue implementation or adjust milestone scope

---

## Step 5: Document Achievements

Only document achievements AFTER validation passes.

Update `milestones/MILESTONES.md` with the completion summary:

### Add Completion Section

Append to the current milestone:

```markdown
### Completion Summary

**Completed:** [date]
**Status:** complete

**Achievements:**
- [Features completed]
- [Nodes implemented]

**Known Limitations:**
- [Known issues]
```

---

## Step 6: Mark Complete

Update `milestones/MILESTONES.md` to mark current milestone complete:

```markdown
## Milestone 1: Core Skeleton
**Status:** complete
```

**After this step:**
- Current milestone is marked complete
- Next milestone remains "planned" (not activated)
- Run `milestone-init` to define contracts for the next milestone

---

## Constraints

- **Does NOT**: Implement features, fix tests, refactor, re-architect, decide scope, activate next milestone
- **Does**: Verify completion, document achievements, mark current complete, report blockers

---

## Success Criteria

- [ ] Current milestone identified
- [ ] Architecture nodes reviewed
- [ ] Node states are acceptable for milestone type
- [ ] Runnable product verified
- [ ] Integration tests exist and cover declared features (or milestone-integrate invoked)
- [ ] Manual verification checklist presented to user (or user chose to skip)
- [ ] Achievements documented in milestones/MILESTONES.md
- [ ] Current milestone marked complete

---

## Next Steps

- **Start next milestone**: Run `milestone-init` to define contracts for the next milestone
- **All complete**: Run full test suite
- **Blocked**: Continue implementation or adjust scope with `milestone-plan-all`
