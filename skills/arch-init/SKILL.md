---
name: arch-init
description: "Initializes architecture documentation with YAML headers and root node. Use when project specification is solid but no architecture exists (ready for architecting)."
---

# Architecture Initialization

## Overview

Initialize the architecture documentation by creating `arch/ARCH_SUMMARY.md` with proper YAML headers and root node definition. This establishes the foundation for subsequent node decomposition.

This skill focuses only on initialization — not decomposition. After initialization, `node-dispatch` will automatically find and decompose the pending root node.

## Prerequisites

The project must have:
1. SPEC.md with complete requirements

## Workflow

1. **Create arch directory** - Ensure `arch/` and `arch/nodes/` directories exist
2. **Define root node** - Identify the system boundary and top-level responsibility
3. **Write ARCH_SUMMARY.md** - Create with YAML headers and root node section
4. **Create root node doc** - Create `arch/nodes/<RootNode>.md` with pending status

---

## Step 1: Create Directories

Create the architecture directory structure:

```
arch/
├── ARCH_SUMMARY.md
└── nodes/
    └── <RootNode>.md
```

---

## Step 2: Define Root Node

Determine the root node:

| Question | Answer |
|----------|--------|
| Name | Project or system name |
| Responsibility | High-level ownership of entire system |
| Boundary | What is inside vs. outside the system |

---

## Step 3: Write ARCH_SUMMARY.md

Create `arch/ARCH_SUMMARY.md` with this structure:

```markdown
---
project: <Project Name>
version: 0.1.0
status: draft

tech_stack:
  language: <Language or "TBD">
  framework: <Framework or "TBD">
  test_framework: <Test Framework or "TBD">
  runtime: <Runtime Model or "TBD">

authoritative_scope: topology_only

editing_rules:
  - This file defines structural tree only.
  - Each node must correspond to a file under arch/nodes/.
  - Do not define detailed interfaces here.
  - Do not embed implementation details.
  - Children must appear under correct heading level.
  - Expanding a node may only modify its subtree section.

reading_guide:
  - Headings represent structural hierarchy.
  - Each node section includes brief responsibility summary.
  - Detailed contracts live in corresponding node documentation files.
---

# <RootNodeName>

Status: pending
Doc: arch/nodes/<RootNodeName>.md

Responsibility:
<1-3 sentence high-level ownership description.>

Dataflow:
- Input: <external sources (e.g., user, API callers)>
- Output: <external consumers (e.g., UI, API responses)>
- Side-effects: <external state changes, if any>

For detailed requirements, see [SPEC.md](../SPEC.md).

---

## Next Steps

- Run `node-dispatch` to begin decomposing the pending root node
```

---

## Step 4: Create Root Node Documentation

Create `arch/nodes/<RootNodeName>.md`:

```markdown
# <RootNodeName>

## Status

pending

## Responsibility

<What this node owns at the system level.>

## Dataflow

### Inputs

- <External sources (e.g., user, API callers)>

### Outputs

- <External consumers (e.g., UI, API responses)>

### Side-effects

- <External state changes, if any>
```

Add other sections as needed for this node.

---

## Constraints

- Do NOT decompose into children — use `node-dispatch` for that
- Do NOT define implementation details

## Success Criteria

- [ ] arch/ directory structure exists
- [ ] ARCH_SUMMARY.md has valid YAML headers
- [ ] Root node defined with responsibility and dataflow
- [ ] Root node doc created at arch/nodes/<RootNode>.md

## Next Steps

After initialization:
- **If milestones/MILESTONES.md exists**: Run `node-decompose` to elaborate the architecture tree
- **If no milestones/MILESTONES.md**: Run `plan-milestones` first, then `node-decompose`
