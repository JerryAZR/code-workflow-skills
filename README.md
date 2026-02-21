# Code Agent Toolkit

> A structural, frontier-driven workflow for building large software systems with AI agents — without collapsing into linear context overload.

---

## Overview

This toolkit provides a collection of Claude Code skills that implement a two-tier architectural model:

- **Outer Tier (Rare, Structural)**: Architecture decisions made infrequently
- **Inner Tier (Frequent, Local)**: Test-driven implementation of individual components

The workflow enforces strict TDD discipline and prevents context overload by keeping each iteration small, local, and bounded.

---

## Skills

### Specification & Planning

| Skill | Description |
|-------|-------------|
| [specify](skills/specify/) | Creates or updates project specifications (SPEC.md) |
| [clarify](skills/clarify/) | Resolves ambiguous areas in specifications through targeted questions |
| [bootstrap](skills/bootstrap/) | Bootstraps new projects with tech stack selection and hello-world baseline |
| [plan-milestones](skills/plan-milestones/) | Plans implementation milestones from specification |

### Architecture

| Skill | Description |
|-------|-------------|
| [arch-init](skills/arch-init/) | Initializes architecture documentation with root node |
| [node-decompose](skills/node-decompose/) | Decomposes architecture nodes into child components |

### Milestone Implementation

| Skill | Description |
|-------|-------------|
| [milestone-init](skills/milestone-init/) | Derives per-node feature requirements for current milestone |
| [node-prep](skills/node-prep/) | Prepares nodes with skeleton code and failing tests |
| [node-build](skills/node-build/) | Implements prepared nodes following TDD workflow |
| [node-test-add](skills/node-test-add/) | Adds tests for modified nodes before milestone wrapup |
| [milestone-integration](skills/milestone-integration/) | Creates integration tests to verify features work together |
| [milestone-wrapup](skills/milestone-wrapup/) | Verifies milestone completion and transitions to next milestone |

### Deprecated

| Skill | Description |
|-------|-------------|
| [node-dispatch](skills/deprecated/node-dispatch/) | DEPRECATED: Use node-decompose directly |

### Issue Management

| Skill | Description |
|-------|-------------|
| [new-issue](skills/new-issue/) | Creates feature request or bug report documents |
| [plan-issue](skills/plan-issue/) | Creates task roadmap with TDD discipline |
| [resolve-issue](skills/resolve-issue/) | Executes issue resolution in batches with review checkpoints |

---

## Workflow

```mermaid
flowchart TB
    subgraph Setup["Setup (One-time)"]
        S1["/specify"] --> S2["/clarify"]
        S2 --> S3["/bootstrap"]
        S3 --> S4["/plan-milestones"]
    end

    subgraph Architecture["Architecture (One-time)"]
        A0["/arch-init"] --> A1["/node-decompose"]
        A1 --> A2{More Nodes?}
        A2 -->|Yes| A1
        A2 -->|No| A3[("Architecture complete")]
    end

    subgraph Implementation["Implementation (Per Milestone)"]
        I1["/milestone-init"] --> I2["/node-prep"]
        I2 --> I3["/node-build"]
        I3 --> I4{More Nodes?}
        I4 -->|Yes| I2
        I4 -->|No| I5["/node-test-add"]
        I5 --> I6["/milestone-integration"]
        I6 --> I7["/milestone-wrapup"]
    end

    subgraph Issue["Issue Management (Optional)"]
        J1["/new-issue"] --> J2["/plan-issue"]
        J2 --> J3["/resolve-issue"]
    end

    Setup --> Architecture
    Architecture -->|All nodes elaborated| Implementation
    I6 -->|More milestones| I1
    I6 -->|All complete| Done[("Done")]
    Implementation -.->|User requests| Issue

    style Setup fill:#e1f5fe
    style Architecture fill:#e8f5e8
    style Implementation fill:#fff3e0
    style Issue fill:#fce4ec
    style Done fill:#e0e0e0
```

### Setup (One-time per project)

```
specify → clarify → bootstrap → plan-milestones
```

1. **specify**: Create SPEC.md with requirements
2. **clarify**: Resolve ambiguities
3. **bootstrap**: Select tech stack and create baseline project
4. **plan-milestones**: Break into manageable milestones

### Architecture (One-time)

```
arch-init → node-decompose (repeat until full tree)
```

1. **arch-init**: Initialize architecture documentation with root node
2. **node-decompose**: Decompose nodes until architecture tree is complete

Run once after Setup to fully elaborate the architecture.

### Implementation (Per Milestone)

```
milestone-init → node-prep → node-build (repeat) → node-test-add → milestone-integration → milestone-wrapup
```

1. **milestone-init**: Define what each node must provide for this milestone
2. **node-prep**: Generate skeleton + failing tests (TDD - red state)
3. **node-build**: Implement to make tests pass (green state)
4. **node-test-add**: Add tests for nodes modified during implementation (should pass)
5. **milestone-integration**: Create integration tests to verify features work together
6. **milestone-wrapup**: Verify completion and transition to next milestone

When milestone is complete, run `milestone-init` for the next milestone.

### Issue Management (Optional)

For bug fixes or feature requests (triggered by user):

```
new-issue → plan-issue → resolve-issue
```

1. **new-issue**: Document the issue
2. **plan-issue**: Create task roadmap with TDD
3. **resolve-issue**: Execute in batches with checkpoints

---

## Node State Model

Architecture nodes progress through these states:

| State | Meaning |
|-------|---------|
| `pending` | Awaiting contract definition (architecture phase) |
| `atomic` | Leaf node in architecture (architecture phase) |
| `decomposed` | Non-leaf node in architecture (architecture phase) |
| `planned` | Node has milestone contract, awaiting preparation |
| `prepared` | Skeleton + failing tests created |
| `implemented` | Logic implemented, tests passing |
| `modified` | Parent implementation changed this node's behavior; needs additional tests |

The toolkit uses a **stable-topology, evolving-contract** approach where:
- Architecture tree is fully elaborated early (all nodes exist from start)
- Nodes start as `pending`, become `atomic` or `decomposed` during architecture
- Entering a new milestone reverts state to `planned` for contract expansion
- `modified` state tracks nodes whose behavior changed during parent implementation

---

## Key Principles

- **Stable topology, evolving contract** - Architecture tree is fully elaborated early and remains fixed; milestones expand what each node must provide
- **One-level decomposition** - Only decompose one level at a time to prevent context explosion
- **TDD enforced** - Tests must fail before implementation; never weaken tests to make them pass
- **Bounded scope** - Each iteration is small, local, and context-efficient
- **Behavioral scope gating** - Scope is controlled by limiting required features, not by hiding nodes
- **Contract invalidation** - When entering a new milestone, node status reverts to `planned` for re-validation; code remains unchanged

---

## Usage

Invoke skills directly using `/skill-name`:

```
/specify build a todo app
/bootstrap Python
/plan-milestones MVP first
/arch-init
/node-decompose
/milestone-init
/node-prep
/node-build
/node-test-add
/milestone-wrapup
/new-issue add dark mode
/plan-issue 001
/resolve-issue 001
```

---

## Scripts

- `scripts/security_scan_all.py` - Run security scans on all skills

```bash
uv run scripts/security_scan_all.py
```
