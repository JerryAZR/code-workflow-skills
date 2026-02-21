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
5. **Manual Verification** - Present checklist for user to verify features (REQUIRED)
6. **Document Achievements** - Record completed work in milestones/MILESTONES.md (only after validation passes)
7. **Transition Milestones** - Mark current complete, next active

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

### Handling Incomplete Work

**If incomplete due to blockers:**
- Do NOT proceed to documentation
- Report what is missing
- Suggest: Continue implementation or adjust milestone scope

**If intentionally incomplete (scope adjustment):**
- May proceed with wrap-up if scope was adjusted

---

## Step 4b: Manual Verification

Present the user with a manual verification checklist.

**If user wants to skip:** Respect their choice and proceed to Step 5.

### Generate Startup Command

Determine how to start/run the application:

| Project Type | Command |
|--------------|---------|
| Python CLI | `python -m <module>` or `python <entrypoint>.py` |
| Node.js CLI | `node <entrypoint>.js` or `npm run start` |
| Web App | `npm run dev` or `python -m flask run` |
| GUI App | Run the built executable |
| Library | N/A (no startup needed) |

### Extract Features

Read the milestone scope from `milestones/MILESTONES.md` to list what features were implemented.

### Present Checklist

Show the user:

```
## Manual Verification Checklist

### How to Start
[command to run]

### Features to Verify
- [ ] Feature 1
- [ ] Feature 2
```

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

After completing a milestone:

1. Read `arch/ARCH_SUMMARY.md`
2. All nodes remain in their current state (`implemented`, `prepared`, etc.)
3. The next `milestone-init` will define new contracts for each node

---

## Constraints

- **Does NOT**: Implement features, fix tests, refactor, re-architect, decide scope
- **Does**: Verify completion, document achievements, transition states, report blockers

---

## Success Criteria

- [ ] Current milestone identified
- [ ] Architecture nodes reviewed
- [ ] Node states are acceptable for milestone type
- [ ] Runnable product verified
- [ ] Manual verification checklist presented to user (or user chose to skip)
- [ ] Achievements documented in milestones/MILESTONES.md
- [ ] Current milestone marked complete
- [ ] Next milestone marked active (if exists)
- [ ] Nodes ready for next milestone's contract (via milestone-init)

---

## Next Steps

- **More milestones**: Run `milestone-init` → `node-prep` → `node-build`
- **All complete**: Run full test suite
- **Blocked**: Continue implementation or adjust scope with `plan-milestones`
