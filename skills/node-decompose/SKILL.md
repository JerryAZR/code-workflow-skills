---
name: node-decompose
description: "Decomposes architecture nodes into child components. Use for expanding any non-leaf node."
argument-hint: "[node-name]"
---

# Node Decompose

## Overview

Perform top-down structural decomposition of an architecture node into well-defined child nodes by refining responsibilities and contracts — without implementing, wiring, or testing anything.

**User's Intent:** $ARGUMENTS

## Prerequisites

- The node must exist in ARCH_SUMMARY.md
- For root decomposition, run `arch-init` first if ARCH_SUMMARY.md does not exist

## Workflow

Follow this process in order:

1. **Read Parent Node** - Get responsibility and dataflow from parent node doc
2. **Clarify Node Responsibility** - Confirm what this node owns
3. **Define Public Contract** - Input/output interfaces
4. **Decompose into Children** - Identify 2-6 cohesive child nodes
5. **Define Child Contracts** - Each child's responsibility and interface
6. **Update Documentation** - Update ARCH_SUMMARY.md and create node docs

---

## Step 1: Read Parent Node

Find the node in ARCH_SUMMARY.md and read its documentation at `arch/nodes/<NodeName>.md`:
- Responsibility: What this node owns
- Dataflow: Inputs, outputs, side-effects

---

## Step 2: Clarify Node Responsibility

For the node being decomposed:

1. **Define single, precise responsibility** - What does this node own?
2. **Define explicit boundaries** - What does this node NOT do?
3. **Identify external interfaces** - How does it interact with the outside world?

---

## Step 3: Define Public Contract

### Input Interface

- What data/events does this node consume?
- User interactions, API requests, file reads, database queries

### Output Interface

- What does this node produce?
- Visual renders, API responses, file writes, data transformations

### Failure Semantics

- How does this node handle errors?
- What invariants must hold?

---

## Step 4: Decompose into Children

Identify 2-6 child nodes that together fulfill the parent node's responsibility:
- Each child owns a portion of what the parent needs to provide
- Children are cohesive (related concerns grouped together)
- Children are orthogonal (minimal overlap in concerns)
- Combined, they cover all parent responsibilities

### Common First-Level Patterns

| System Type | Common Children |
|-------------|-----------------|
| Web Application | UI Layer, API Layer, Data Layer |
| CLI Tool | CLI Parser, Core Engine, Output Formatter |
| Microservice | API Handler, Business Logic, Data Access |
| Library | Public API, Internal Core |
| Gateway | Routing, Protocol Translation, Auth |

### Structural Dependencies vs Data Movement

**Structural dependencies** (who owns or controls state) must form a tree (acyclic):
- Parent nodes own or control resources that child nodes use
- Example: API Layer depends on Business Logic, which depends on Data Access

**Data movement** (inputs/outputs of a node) is separate and often bidirectional:
- UI receives user events (input) and renders visual updates (output)
- Functions receive arguments (input) and return values (output)
- Event handlers receive events (input) and emit responses (output)
- **Bidirectional flows are normal and do not indicate circular dependencies**

Do not force nodes into an acyclic structure to accommodate normal bidirectional data flows.

---

## Step 5: Define Child Contracts

The parent node defines what each child must provide. For each child node, define:

| Property | Description |
|----------|-------------|
| Name | Clear, concise node name |
| Responsibility | What this child must own to fulfill parent's needs |
| Input | What the parent will provide to this child |
| Output | What this child must return to the parent |
| Contract | How parent and child interact (interfaces, protocols) |

---

## Step 6: Update Documentation

### Update ARCH_SUMMARY.md

Add child nodes under the parent node heading in `arch/ARCH_SUMMARY.md`:

```markdown
## <ParentNode>

... existing content ...

## <ChildNode1>

Status: pending
Doc: arch/nodes/<ChildNode1>.md

Responsibility:
<1-3 sentence summary of this child's purpose.>

Dataflow:
- Input: <what this child consumes>
- Output: <what this child produces>
- Side-effects: <external state changes, if any>

---

## <ChildNode2>

Status: pending
Doc: arch/nodes/<ChildNode2>.md

Responsibility:
<Short description.>

---
```

### Create Node Documentation

For each node, create documentation at `arch/nodes/<NodeName>.md`:

```markdown
# <NodeName>

## Status

pending | decomposed | implemented

## Responsibility

<What this node owns and is accountable for.>

## Dataflow

### Inputs

- <What this node consumes>

### Outputs

- <What this node produces>

### Side-effects

- <External state changes, if any>
```

The decomposer decides what additional sections (APIs, Events, Configuration, Dependencies, Invariants) are needed based on node type and responsibility.

---

## Constraints

### What This Skill Does NOT Do

- Implementation - No code, algorithms, or data structures
- Wiring - Don't connect children together
- Testing - Don't create test stubs
- Deep design beyond first level - Only define immediate children
- Prioritization - Don't assign order to components

---

## Success Criteria

- [ ] Node responsibility is clear and bounded
- [ ] Children are cohesive and orthogonal (2-6 children)
- [ ] All parent responsibilities map to children
- [ ] Structural dependencies form a tree
- [ ] Bidirectional data flows documented (inputs/outputs/side-effects)
- [ ] ARCH_SUMMARY.md updated with child nodes
- [ ] Each child has documentation file

## Next Steps

After decomposition:
- If the decomposition needs refinement - Re-run `node-decompose`
- If ready to implement a node - Use node-prep and node-build
