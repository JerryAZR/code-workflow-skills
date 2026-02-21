---
name: plan-milestones
description: "Plans implementation milestones by ordering features from basic skeleton to highest priority. Use when a project needs to be broken down into manageable implementation phases."
argument-hint: "[milestone focus or priority]"
---

# Milestone Planning

## Overview

Transform a project specification into ordered implementation milestones. Start with the basic system skeleton, then progressively add features from highest to lowest priority. Limit each milestone scope to ensure manageable, testable increments.

This skill is architecture-agnostic—it plans in terms of user-facing features, not internal architecture nodes.

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides an argument (e.g., "MVP first" or "API focus"), treat it as the priority focus. Try to satisfy directly. If unclear, ask clarifying questions.

## Prerequisites

This skill works from the specification:

1. **Specification exists** - `SPEC.md` must exist with feature requirements

## Workflow

Follow this process in order:

1. **Analyze specification** - Review SPEC.md to understand features
2. **Enumerate features** - List all features from the spec
3. **Clarify priorities** - Ask user if feature priorities are unclear
4. **Define milestone scope** - Limit each milestone to 3-5 features maximum
5. **Order milestones** - Skeleton first, then by priority descending
6. **Document milestone plan** - Create `milestones/MILESTONES.md`

## Step 1: Analyze Specification

Read the specification to understand the full scope:

1. Read `SPEC.md` to identify all features and requirements
2. Note any explicit priorities mentioned in the spec
3. Identify dependencies between features

## Step 2: Enumerate Features

Extract all features from the specification:

**Create a feature list:**
- Core functionality (must work for system to be useful)
- User-facing features (what users can do)
- Integration points (external services, APIs)
- Non-functional requirements (performance, security)

**Do not:**
- Map features to architecture nodes
- Consider implementation details
- Worry about technical dependencies yet

## Step 3: Clarify Priorities

If priorities are unclear, ask the user:

```
I need to clarify feature priorities:

1. Which features are essential for the first usable release?
2. Which features can wait until later versions?
3. Are there features that depend on others being complete first?

Please categorize:
- Must-have (MVP): [list features]
- Should-have (v1.0): [list features]
- Could-have (future): [list features]
```

## Step 4: Define Milestone Scope

Create milestones with limited scope:

**Each milestone should include:**
- 3-5 related features maximum
- Cohesive theme (all features serve a common goal)
- Deliverable at the end (runnable, testable)

**Guidelines:**
- First milestone = skeleton (minimal working system)
- Subsequent milestones = progressive enhancement
- Avoid milestones > 5 features (too large to manage)

## Step 5: Order Milestones

Order by:
1. **Skeleton first** - Core infrastructure and basic flow
2. **Priority descending** - Highest priority features next
3. **Dependency respect** - Ensure prerequisites come first

## Step 6: Document Milestone Plan

Create `milestones/MILESTONES.md` (create `milestones/` directory if it doesn't exist):

**Important:** Mark the first milestone as "in-progress" to signal that work can begin immediately:

```markdown
# Milestone Plan

## Milestone 1: Core Skeleton
**Status:** in-progress
**Target:** Minimal working system

### Features
- Feature A: Basic input handling
- Feature B: Core processing
- Feature C: Simple output

### Scope
- Minimal viable functionality
- No advanced features
- Basic happy path only

### Success Criteria (User-Observable)
- [ ] App starts / library imports / CLI runs
- [ ] Features in scope are usable
- [ ] User can verify each feature works manually

---

## Milestone 2: Core Features
**Status:** planned
**Target:** Primary user functionality

### Features
- Feature D: User authentication
- Feature E: Main user interface
- Feature F: Data persistence

### Scope
- Primary use cases implemented
- Error handling for common cases
- Basic validation

### Success Criteria (User-Observable)
- [ ] Core features are usable
- [ ] Users can accomplish main tasks
- [ ] User can verify features work manually

---

## Milestone 3: Enhancement
**Status:** planned
**Target:** Additional capabilities

### Features
- Feature G: Advanced search
- Feature H: User preferences
- Feature I: Performance optimization

### Scope
- Advanced functionality
- Performance optimization
- Enhanced user experience

### Success Criteria (User-Observable)
- [ ] Enhanced features are usable
- [ ] Performance improvements are observable
- [ ] User can verify improvements manually
```

## Constraints

### What This Skill Does NOT Do

- Reference architecture nodes (architecture-agnostic)
- Define detailed implementation order (that's node-build's job)
- Specify exact timelines or dates
- Create test plans (defer to node-prep)
- Implement any code

## Success Criteria

- [ ] SPEC.md analyzed completely
- [ ] All features enumerated
- [ ] Priorities clarified with user
- [ ] Each milestone has 3-5 features
- [ ] Milestone 1 is the skeleton
- [ ] Ordering respects dependencies
- [ ] milestones/MILESTONES.md created
- [ ] Each milestone has user-observable success criteria

## Next Steps

After milestone planning:

- **Initialize architecture** - Run `arch-init` to create the architecture skeleton
- **Begin decomposition** - Run `node-decompose` to decompose pending nodes relevant to Milestone 1
- **Continue dispatching** - Re-run `node-decompose` to handle more pending nodes
- **Refine if needed** - Adjust scope based on implementation experience
