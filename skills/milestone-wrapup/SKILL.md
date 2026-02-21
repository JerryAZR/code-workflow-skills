---
name: milestone-wrapup
description: "Wraps up the current milestone by verifying implementation progress, documenting achievements, and transitioning to the next milestone. Use when a milestone's work is complete and ready for review."
argument-hint: "[milestone-number]"
---

# Milestone Wrap-up

## Overview

Verify that the current milestone is complete, document what has been achieved, and prepare for the next milestone.

**User's Intent:** $ARGUMENTS

This skill ensures milestone completion follows a consistent process with proper verification and documentation.

## Prerequisites

- `milestones/MILESTONES.md` exists with milestone definitions
- `arch/ARCH_SUMMARY.md` exists with node states (if architecture exists)

## Workflow

Follow this process in order:

1. **Read Milestone Plan** - Identify current milestone and its scope
2. **Review Architecture Progress** - Check node states in ARCH_SUMMARY.md
3. **Verify Deliverables** - Confirm runnable product or usable library exists
4. **Validate Completeness** - Ensure all required work is done
5. **Document Achievements** - Record completed work in milestones/MILESTONES.md (only after validation passes)
6. **Transition Milestones** - Mark current complete, next active

---

## Step 1: Read Milestone Plan

Read `milestones/MILESTONES.md` to understand:

1. **Current milestone** - Which milestone is in-progress (or specified)
2. **Milestone scope** - What features are included
3. **Success criteria** - What must be complete to wrap up
4. **Next milestone** - What comes after (if any)

If no milestone number provided, find the in-progress milestone (status: "in-progress").

**Error Handling:**
- If `milestones/MILESTONES.md` does not exist, report: "No milestone plan found. Create one using plan-milestones skill first."
- If no in-progress milestone exists, report: "No milestone is currently in-progress. Use plan-milestones to create one."

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

Note: The new model uses stable topology - all nodes exist. Scope is controlled by each node's milestone contract, not by node states.

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

Execute the appropriate verification based on project type:

**For Libraries:**
- Verify the library can be imported
- Verify public API is accessible

```bash
# Python library
python -c "import src; print('Import OK')"

# Node.js library
node -e "require('./src'); console.log('OK')"
```

**For CLI Tools:**
- Verify CLI command is invokable
- Verify help/usage works

```bash
# Python CLI
python -m <module> --help

# Node.js CLI
node ./src/cli.js --help

# Installed CLI
<command> --help
```

**For GUI Applications:**
- Verify GUI window can be created (even if empty)
- Verify application starts without crash

```bash
# Python (Tkinter, PyQt, etc.)
python -c "import tkinter; tkinter.Tk().destroy()"

# Electron
ls dist/*.exe || ls build/*.exe

# Check for build output
ls <dist-folder>/
```

**Error Handling:**
- If no runnable product exists and milestone requires one, report: "No runnable product found. Complete implementation before wrap-up."
- If verification fails for any project type, report the specific failure

---

## Step 4: Validate Completeness

Perform final checks before marking milestone complete:

### Checklist

- [ ] All required nodes are in acceptable states
- [ ] Runnable product exists and works
- [ ] Milestone scope is fulfilled
- [ ] No critical blockers remain

### Handling Incomplete Work

**If incomplete due to blockers:**
- Do NOT proceed to documentation
- Report what is missing
- Suggest: Continue implementation or adjust milestone scope

**If intentionally incomplete (scope adjustment):**
- May proceed with wrap-up if scope was adjusted

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

#### Achievements
- [List specific features completed]
- [List architecture nodes implemented]
- [List any notable improvements]

#### Known Limitations
- [Any known issues]
- [Technical debt notes]

#### Verification

**Project Type:** [library/cli/gui/web/API]

**Runnable:** [yes/no]
- [Library imports successfully]
- [CLI command works]
- [GUI window appears]

**Tests:** [yes/no]
- [Unit tests pass]
- [Integration tests pass]

**Documentation:** [yes/no]
- [README updated]
- [API docs updated]
- [Usage examples added]
```

---

## Step 6: Transition Milestones

Update `milestones/MILESTONES.md` to mark completion:

### Mark Current Milestone Complete

```markdown
## Milestone 1: Core Skeleton
**Status:** complete
```

### Activate Next Milestone (if exists)

```markdown
## Milestone 2: Feature Addition
**Status:** in-progress
```

### If No Next Milestone

```markdown
## All Milestones Complete
**Status:** complete
```

### Contract Invalidation for Next Milestone

In the stable-topology, evolving-contract model, node contracts change per milestone. After completing a milestone:

1. Read `arch/ARCH_SUMMARY.md`
2. All nodes remain in their current state (`implemented`, `prepared`, etc.)
3. The next `milestone-init` will define new contracts for each node

**Rationale:** Architecture topology is stable - nodes don't get deferred. Each milestone defines what capabilities each node must provide. The contract expansion drives re-validation, not structural changes.

---

## Constraints

### What This Skill Does NOT Do

- Implement incomplete features
- Fix failing tests
- Refactor code
- Re-architect nodes
- Decide milestone scope (that's plan-milestones' job)

### What This Skill Does

- Verify completion status
- Document achievements
- Transition milestone states
- Report blockers

---

## Success Criteria

- [ ] Current milestone identified
- [ ] Architecture nodes reviewed
- [ ] Node states are acceptable for milestone type
- [ ] Runnable product verified
- [ ] Achievements documented in milestones/MILESTONES.md
- [ ] Current milestone marked complete
- [ ] Next milestone marked active (if exists)
- [ ] Nodes ready for next milestone's contract (via milestone-init)

---

## Next Steps

After milestone wrap-up:

### If More Milestones Remain
- **Define contracts**: Run `milestone-init` to derive node capabilities for next milestone
- **Implement**: Run `node-prep` and `node-build` for each node

### If All Complete
- **Celebrate**: Project milestone completion
- **Review**: Run full test suite and verification

### If Blocked
- **Continue implementation**: Use node-build to complete remaining nodes
- **Adjust scope**: Use plan-milestones to update milestone definitions
