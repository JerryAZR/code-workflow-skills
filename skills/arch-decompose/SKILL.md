---
name: arch-decompose
description: "Decomposes architecture nodes into child components. Use for expanding any pending non-leaf node. If no node specified, auto-detects first pending node from ARCH_SUMMARY.md."
argument-hint: "[node-name]"
---

# Architecture Decompose

## Overview

Perform top-down structural decomposition of an architecture node into well-defined child nodes by refining responsibilities and contracts — without implementing, wiring, or testing anything.

**User's Intent:** $ARGUMENTS

If no node-name provided, find the first "pending" node in `arch/ARCH_SUMMARY.md` and decompose that.

## Prerequisites

- The node must exist in ARCH_SUMMARY.md with "pending" status
- For root decomposition, run `arch-init` first if ARCH_SUMMARY.md does not exist

## Workflow

Follow this process in order:

1. **Resolve Target Node** - If no argument, find first "pending" node in ARCH_SUMMARY.md
2. **Read Parent Node** - Get responsibility and dataflow from parent node doc
3. **Clarify Node Responsibility** - Confirm what this node owns
4. **Decide: Decompose or Atomic** - Determine if node should be decomposed or marked atomic
5. **Define Child Contracts** - Each child's responsibility and interface (if decomposing)
6. **Update Documentation** - Update ARCH_SUMMARY.md, mark current node, create child docs

---

## Step 1: Resolve Target Node

If no node-name argument provided:
1. Read `arch/ARCH_SUMMARY.md`
2. Find the first node with "Status: pending"
3. Use that node as the target for decomposition

If node-name provided, verify it exists in ARCH_SUMMARY.md with "pending" status.

**Determining node path:** The node's documentation path is derived from its heading level in ARCH_SUMMARY.md:
- Root node (##) → `arch/nodes/<RootNode>.md`
- Level 2 child (###) → `arch/nodes/<ParentNode>/<ChildNode>.md`
- Level 3 child (####) → `arch/nodes/<ParentNode>/<ChildNode>/<GrandChild>.md`
- And so on...

---

## Step 2: Read Parent Node

Find the node in ARCH_SUMMARY.md and read its documentation at `arch/nodes/<NodePath>/<NodeName>.md`:
- Responsibility: What this node owns
- Dataflow: Inputs, outputs, side-effects

---

## Step 3: Clarify Node Responsibility

For the node being decomposed:

1. **Define single, precise responsibility** - What does this node own?
2. **Define explicit boundaries** - What does this node NOT do?
3. **Identify external interfaces** - How does it interact with the outside world?

---

## Step 4: Decide - Decompose or Atomic

### Status Options

| Status | Meaning |
|--------|--------|
| pending | Node awaiting decomposition |
| decomposed | Has child nodes defined |
| atomic | Single-focus responsibility, should not decompose further |
| implemented | Logic ready, tests passed |

### Decision Criteria

Mark node as **atomic** if it has a clear, single-focus responsibility that makes no sense to decompose further:
- The responsibility is already well-scoped and cohesive
- Further decomposition would add unnecessary complexity
- The node represents a concrete, implementable unit

Mark node as **decomposed** if it needs child nodes to fulfill its responsibility.

### Atomic Nodes

When marking a node as atomic:
1. Update status to "atomic" in ARCH_SUMMARY.md (this is a leaf node - it has no children)
2. Polish the node doc with detailed responsibility and contracts
3. No child nodes are created - this node is done being decomposed

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

### 1. Update Current Node Status

In `arch/ARCH_SUMMARY.md`, change the target node's status:

- If decomposed into children: Change from "pending" to "decomposed"
- If atomic: Change from "pending" to "atomic"

### 2. Update Current Node Doc

Polish the current node's documentation at `arch/nodes/<NodePath>/<NodeName>.md`:
- Add more detail to responsibility (best-effort, don't overthink)
- Clarify input/output interfaces
- Add any additional sections that feel necessary
- The details will be ironed out during implementation

### 3. Add Child Nodes to ARCH_SUMMARY.md

Add child nodes under the parent node heading in `arch/ARCH_SUMMARY.md`. **Children must be one heading level deeper than parent** (if parent is ##, children are ###):

```markdown
## <ParentNode>

Status: decomposed | atomic
Doc: arch/nodes/<ParentNode>.md

... existing content ...

### <ChildNode1>

Status: pending
Doc: arch/nodes/<ParentNode>/<ChildNode1>.md

Responsibility:
<1-3 sentence summary of this child's purpose.>

Dataflow:
- Input: <what this child consumes>
- Output: <what this child produces>
- Side-effects: <external state changes, if any>

---

### <ChildNode2>

Status: pending
Doc: arch/nodes/<ParentNode>/<ChildNode2>.md

Responsibility:
<Short description.>

---
```

**Note:** Child nodes are always "pending" — never create a child directly in "atomic" state.

### 4. Create Child Node Docs

Create a subdirectory `arch/nodes/<ParentNode>/` and add child node docs there:

```markdown
# <ChildNodeName>

## Responsibility

<What this child owns.>

## Contract

### Input

<What the parent provides.>

### Output

<What the child returns to parent.>
```

Add other sections only if clearly needed — details will be refined during implementation.

---

## Constraints

### Scope: Structural Only

Node documentation created here defines **what the node IS**:
- Responsibility: What this node owns at the architecture level
- Dataflow: Input sources, output destinations, side-effects
- Contract: How parent and child interact (interfaces, protocols)

**DO NOT include:**
- Capabilities or features sections (these belong in milestone capabilities.md)
- Behavioral requirements (these are added per-milestone)
- Implementation details

### What This Skill Does NOT Do

- Implementation - No code, algorithms, or data structures
- Wiring - Don't connect children together
- Testing - Don't create test stubs
- Deep design beyond first level - Only define immediate children
- Prioritization - Don't assign order to components

---

## Success Criteria

- [ ] Target node resolved (from argument or first pending in ARCH_SUMMARY.md)
- [ ] Node responsibility is clear and bounded
- [ ] Decision made: decomposed or atomic
- [ ] If decomposed: Children are cohesive and orthogonal (2-6 children)
- [ ] Current node status updated to "decomposed" or "atomic"
- [ ] Current node doc polished with more detail (best-effort)
- [ ] Child nodes added to ARCH_SUMMARY.md with "pending" status
- [ ] Each child has minimal documentation (responsibility + contract)

## Next Steps

- **To continue decomposition**: Run `arch-decompose` to find and decompose the next pending node relevant to current milestone
- **To decompose specific node**: Run `arch-decompose <node-name>` for a particular node (if pending)
- **If all nodes decomposed**: When no more pending nodes exist, run `milestone-init` to begin the Implementation phase
