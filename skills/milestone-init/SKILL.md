---
name: milestone-init
description: "Derives and documents per-node feature requirements for the current milestone. Run before each milestone begins to define what each architecture node must provide."
argument-hint: "[milestone-name]"
---

# Milestone Init

## Overview

Derives and documents what each architecture node must provide for the current milestone. This establishes the behavioral scope for the milestone — each node's contract is explicitly defined before implementation begins.

This skill defines per-node capability requirements:
- Architecture topology is fixed (all nodes exist)
- Each milestone defines which capabilities each node must provide
- Scope is behavioral, not structural

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides a milestone-name, verify it exists in `milestones/MILESTONES.md`. If not provided, use the current "in-progress" milestone, or the next "planned" milestone.

## Prerequisites

- `milestones/MILESTONES.md` exists
- `arch/ARCH_SUMMARY.md` exists with architecture nodes
- Run `milestone-plan-all` first to create milestone plan
- Run `arch-init` and `arch-decompose` to create architecture

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
- If `milestones/MILESTONES.md` does not exist, inform: "No milestones found. Run `milestone-plan-all` first."
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

**Note:** Each capability must contribute to user-observable deliverables (features the user can run/use and verify manually). If a capability cannot be traced to a user-observable feature, reconsider its necessity for this milestone.

### Output Format

Create per-node capability documents at `milestones/{name}/nodes/{NodePath}.md`:

**File:** `milestones/{name}/nodes/{NodeName}.md`

```markdown
# {NodeName} - Milestone {N}

**Base Responsibility:** See ../../arch/nodes/{NodePath}.md

## Milestone Contract

- {capability 1}
- {capability 2}

## Supported Features

- {feature from milestone}

## Expected Tests

- {test that verifies capability}
```

**Overview file:** `milestones/{name}/capabilities.md`

```markdown
# {Milestone Name} - Node Capabilities

## Overview

**Milestone:** {index}. {name}
**Status:** in-progress

## Node Capabilities

| Node | File |
|------|------|
| {NodeName} | nodes/{NodeName}.md |
```

Each per-node file **extends** arch/nodes/ with behavioral requirements — it does NOT replace the structural contract.

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
- If any node has state `pending` → Stop and report: "Architecture not fully elaborated. Some nodes still have 'pending' state. Complete arch-decompose first."
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

## Manual Verification Checklist

### How to Start

| Project Type | Command |
|--------------|---------|
| Python CLI | `python -m <module>` or `python <entrypoint>.py` |
| Node.js CLI | `node <entrypoint>.js` or `npm run start` |
| Web App | `npm run dev` or `python -m flask run` |
| GUI App | Run the built executable |
| Library | N/A (no startup needed) |

### Features to Verify

- {feature 1 from milestone}
- {feature 2 from milestone}

## Verification

After implementation, each node's tests should verify these capabilities.
```

### Directory Structure

If `milestones/` directory doesn't exist, create it:

```
milestones/
├── MILESTONES.md
└── {index}-{name}/
    ├── capabilities.md          # Overview + index
    └── nodes/
        ├── {NodeName}.md       # Per-node capabilities
        └── {NodeName}.md
```

Mirror the `arch/nodes/` directory structure for easy reference.

---

## Constraints

### Scope: Behavioral Only

Capabilities.md defines **what the node MUST DO** for this milestone:
- Specific capabilities the node must provide
- Features being implemented
- Expected tests that verify behavior

**DO NOT include:**
- Redefining structural responsibility (that's in arch/nodes/)
- Input/output contract details (that's in arch/nodes/)
- Implementation approach (that's decided during node-prep/node-build)

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
- [ ] Capabilities contribute to user-observable deliverables
- [ ] Node states updated to "planned" for contract expansion
- [ ] Capabilities overview created at milestones/{index}-{name}/capabilities.md
- [ ] Per-node capabilities created at milestones/{index}-{name}/nodes/{NodeName}.md

## Next Steps

After milestone-init completes:
- **Prepare nodes**: Run `node-prep` to create failing tests for each node's capabilities
