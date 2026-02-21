---
name: milestone-init
description: "Derives and documents per-node feature requirements for the current milestone. Run before each milestone begins to define what each architecture node must provide."
argument-hint: "[milestone-name]"
---

# Milestone Init

## Overview

Derives and documents what each architecture node must provide for the current milestone. This establishes the behavioral scope for the milestone — each node's contract is explicitly defined before implementation begins.

This skill implements **explicit capability layers** from the stable-topology, evolving-contract model:
- Architecture topology is fixed (all nodes exist)
- Each milestone defines which capabilities each node must provide
- Scope is behavioral, not structural

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides a milestone-name, verify it exists in `milestones/MILESTONES.md`. If not provided, use the current "in-progress" milestone, or the next "planned" milestone.

## Prerequisites

- `milestones/MILESTONES.md` exists
- `arch/ARCH_SUMMARY.md` exists with architecture nodes
- Run `plan-milestones` first to create milestone plan
- Run `arch-init` and `node-decompose` to create architecture

## Workflow

Follow this process in order:

1. **Identify Current Milestone** - Find the active or next milestone
2. **Gather Milestone Features** - Extract features from milestones/MILESTONES.md
3. **Gather Architecture Nodes** - Get all nodes from ARCH_SUMMARY.md
4. **Derive Node Capabilities** - Map features to node responsibilities
5. **Update Node States** - Set implemented nodes to "planned" for contract expansion
6. **Document Capabilities** - Create milestone-specific capability document

---

## Step 1: Identify Current Milestone

Read `milestones/MILESTONES.md` to find the milestone to initialize:

1. Look for milestone with status "in-progress"
2. If none, find the first milestone with status "planned"
3. Extract the milestone name and index

**If picking a "planned" milestone:**
- Change its status from "planned" to "in-progress"
- Update `milestones/MILESTONES.md` to reflect this change

**Error Handling:**
- If `milestones/MILESTONES.md` does not exist, inform: "No milestones found. Run `plan-milestones` first."
- If no milestone has "in-progress" or "planned" status, ask user to activate a milestone.

---

## Step 2: Gather Milestone Features

Extract all features from `milestones/MILESTONES.md`:

1. List each feature under the milestone
2. Note any acceptance criteria or requirements
3. Understand what the milestone aims to deliver

---

## Step 3: Gather Architecture Nodes

Read `arch/ARCH_SUMMARY.md` to get all architecture nodes:

1. List all nodes (both atomic and decomposed)
2. Note each node's responsibility and dataflow
3. Include parent-child relationships

---

## Step 4: Derive Node Capabilities

For each node, determine what capabilities it must provide for this milestone:

### Process

For each node, analyze:
1. Which milestone features does this node support?
2. What data must this node process?
3. What interfaces must this node expose?
4. What are its integration points?

### Output Format

For each node, document:

```
## {NodeName}

**Milestone Contract:**
- {capability 1}
- {capability 2}
- ...

**Supported Features:**
- {feature from milestone}

**Expected Tests:**
- {test that verifies capability}
```

### Decision Rules

- If a node supports any feature in the milestone → it has a contract for this milestone
- If a node has no features in the milestone → it has "pass-through" contract (just passes data)
- Infrastructure nodes (logging, config) always have basic capabilities

---

## Step 5: Update Node States

After deriving capabilities, update node states in `arch/ARCH_SUMMARY.md`:

For each node with a contract for this milestone:

| Current State | New State | Reason |
|---------------|-----------|--------|
| `implemented` | `planned` | Contract has expanded, needs re-validation |
| `modified` | `planned` | Contract has expanded, needs re-validation |
| `decomposed` | `planned` | Ready for implementation |
| `atomic` | `planned` | Ready for implementation |

**Error Handling:**
- If any node has state `pending` → Stop and report: "Architecture not fully elaborated. Some nodes still have 'pending' state. Complete node-decompose first."
- If any node has state `prepared` → Stop and report: "Previous milestone incomplete. Some nodes still have 'prepared' state. Complete the current milestone (node-prep + node-build + milestone-wrapup) before starting a new one."

This is the **contract invalidation** concept: when entering a new milestone, nodes that were implemented may now need to provide new capabilities, so their state reverts to `planned` for re-validation.

---

## Step 6: Document Capabilities

Create a milestone capabilities document at `milestones/{index}-{name}/capabilities.md`:

```markdown
# {Milestone Name} - Node Capabilities

This document defines what each architecture node must provide for this milestone.

## Overview

**Milestone:** {index}. {name}
**Status:** in-progress

## Node Contracts

{Node 1}
{Node 2}
...

## Verification

After implementation, each node's tests should verify these capabilities.
```

### Directory Structure

If `milestones/` directory doesn't exist, create it:
```
milestones/
  MILESTONES.md
  {index}-{name}/
    capabilities.md
```

---

## Constraints

### What This Skill Does

- Creates explicit per-node contracts for the milestone
- Documents capabilities in a verifiable format
- Sets up behavioral scope boundaries

### What This Skill Does NOT Do

- Modify ARCH_SUMMARY.md topology
- Implement any node - use node-prep/node-build for that
- Modify milestones/MILESTONES.md (except to activate milestone if needed)

---

## Success Criteria

- [ ] Current milestone identified
- [ ] All features extracted from milestones/MILESTONES.md
- [ ] All nodes gathered from ARCH_SUMMARY.md
- [ ] Each node has documented capabilities
- [ ] Node states updated to "planned" for contract expansion
- [ ] Capabilities document created at milestones/{index}-{name}/capabilities.md

## Next Steps

After milestone-init completes:
- **Prepare nodes**: Run `node-prep` to create failing tests for each node's capabilities
