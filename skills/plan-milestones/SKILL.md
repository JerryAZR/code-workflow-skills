---
name: plan-milestones
description: "Plans implementation milestones from architecture by ordering features from basic skeleton to highest priority. Use when architecture is defined and needs to be broken down into manageable implementation phases."
argument-hint: "[architecture summary or milestone focus]"
---

# Milestone Planning

## Overview

Transform the defined architecture into ordered implementation milestones. Start with the basic system skeleton, then progressively add features from highest to lowest priority. Limit each milestone scope to ensure manageable, testable increments.

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides an argument (e.g., "MVP first" or "API focus"), treat it as the priority focus. Try to satisfy directly. If unclear, ask clarifying questions.

## Prerequisites

Before invoking this skill, ensure:

1. **Architecture exists** - `arch/ARCH_SUMMARY.md` must exist with the node hierarchy (invoke `root-architect`)
2. **Node documentation exists** - All first-level nodes have documentation files
3. **Tech stack is chosen** - The project must have a documented tech stack in SPEC.md (invoke `bootstrap`)

## Hard Gates

<HARD-GATE>
Do NOT proceed if architecture is not defined. Invoke `root-architect` first.
</HARD-GATE>

<HARD-GATE>
Do NOT create milestones for features not in the architecture.
</HARD-GATE>

## Workflow

Follow this process in order:

1. **Analyze architecture** - Review ARCH_SUMMARY.md and node documents
2. **Identify feature layers** - Separate core skeleton from enhancement features
3. **Clarify priorities** - Ask user if feature priorities are unclear
4. **Define milestone scope** - Limit each milestone to 2-4 nodes maximum
5. **Order milestones** - Skeleton first, then by priority descending
6. **Document milestone plan** - Create `arch/MILESTONES.md`

## Step 1: Analyze Architecture

Read the architecture to understand the full scope:

1. Read `arch/ARCH_SUMMARY.md` to see all nodes
2. Read each node's documentation to understand dependencies
3. Identify which nodes are essential (skeleton) vs optional (enhancements)

## Step 2: Identify Feature Layers

Categorize nodes into layers:

**Layer 1 - Core Skeleton (always first):**
- Essential infrastructure nodes
- Basic data flow paths
- Minimal viable interfaces

**Layer 2 - High Priority Features:**
- Critical user-facing functionality
- Core business logic
- Essential integrations

**Layer 3 - Lower Priority Features:**
- Nice-to-have functionality
- Advanced features
- Non-critical integrations

## Step 3: Clarify Priorities

If the architecture doesn't clearly indicate priority, ask the user:

```
I need to clarify the priority of some features:

1. Which features are essential for the first usable release?
2. Which features can wait until later versions?
3. Are there any features that depend on others being complete first?

Please identify:
- Must-have (MVP): [list features]
- Should-have (v1.0): [list features]
- Could-have (future): [list features]
```

## Step 4: Define Milestone Scope

Create milestones with limited scope:

**Each milestone should include:**
- 2-4 related nodes maximum
- Clear dependency chain (no blocked nodes)
- Deliverable at the end (runnable, testable)

**Guidelines:**
- First milestone = skeleton (minimal working system)
- Subsequent milestones = progressive enhancement
- Avoid milestones > 4 nodes (too large to manage)

## Step 5: Order Milestones

Order by:
1. **Skeleton first** - Core infrastructure and basic flow
2. **Priority descending** - Highest priority features next
3. **Dependency respect** - Ensure prerequisites come first

## Step 6: Document Milestone Plan

Create `arch/MILESTONES.md`:

```markdown
# Milestone Plan

## Milestone 1: Core Skeleton
**Status:** planned
**Target:** Minimal working system

### Nodes
- NodeA (infrastructure)
- NodeB (core interface)

### Scope
- Basic data flow from input to output
- Core interfaces defined
- No advanced features

### Success Criteria
- [ ] System compiles and runs
- [ ] Basic happy path works
- [ ] Interfaces documented

---

## Milestone 2: Core Features
**Status:** planned
**Target:** Primary functionality

### Nodes
- NodeC (business logic)
- NodeD (user features)

### Scope
- Primary use cases implemented
- Error handling for common cases

### Success Criteria
- [ ] Core features functional
- [ ] Basic error handling works

---

## Milestone 3: Enhancement
**Status:** planned
**Target:** Additional capabilities

### Nodes
- NodeE (advanced features)
- NodeF (nice-to-have)

### Scope
- Advanced functionality
- Performance optimization

### Success Criteria
- [ ] Enhanced features work
- [ ] Performance targets met
```

## Constraints

### What This Skill Does NOT Do

- Define detailed implementation order (that's node-build's job)
- Specify exact timelines or dates
- Create test plans (defer to node-prep)
- Implement any code

### What Future Work Can Do

- Refine milestone scope based on implementation experience
- Adjust ordering based on discovered dependencies
- Add new milestones as requirements evolve

## Success Criteria

- [ ] Architecture analyzed completely
- [ ] Features categorized into layers
- [ ] Priorities clarified with user
- [ ] Each milestone has 2-4 nodes
- [ ] Milestone 1 is the skeleton
- [ ] Ordering respects dependencies
- [ ] MILESTONES.md created

## Next Steps

After milestone planning:

- **Implement Milestone 1** - Use `node-prep` then `node-build` for each node
- **Refine if needed** - Adjust scope based on implementation experience
- **Parallel tracks** - Multiple milestones can be prepared in parallel
