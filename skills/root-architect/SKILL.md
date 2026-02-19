---
name: root-architect
description: "Creates initial shallow architectural topology by decomposing specifications into root node and first-level components. Use when a project has a clear specification and needs its system architecture defined."
argument-hint: "[project description or spec file]"
---

# Root-Level Architect

## Overview

Produce the system's initial shallow architectural topology by decomposing the clarified specification into a root node and a bounded set of first-level components. Write `ARCH_SUMMARY.md` to reflect the tree structure using the predefined header template, and generate corresponding node documentation files.

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides an argument (e.g., a project description or spec file path), treat it as user input. Try to satisfy the request directly. If the request seems unclear or suboptimal, clearly argue against it with alternatives. If the user has settled on a decision, respect it and make it work.

## Workflow

Follow this process in order:

1. **Verify prerequisites** - Ensure specification and tech stack are documented
2. **Analyze specification** - Understand requirements, user flows, and constraints
3. **Define root node** - Identify the system boundary and top-level responsibility
4. **Decompose to first level** - Identify 2-6 cohesive first-level components
5. **Verify coverage** - Ensure all requirements map to nodes
5.5. **Clarify dataflow** - Annotate inputs, outputs, and side-effects per node
6. **Write ARCH_SUMMARY.md** - Create summary using template
7. **Generate node docs** - Create documentation for each node

## Step 1: Verify Prerequisites

Check that the project has:
1. A complete `SPEC.md` with clear scope (invoke `specify`)
2. A documented Tech Stack section in SPEC.md (invoke `bootstrap`)
3. No `[NEEDS CLARIFICATION]` markers (invoke `clarify`)

## Step 2: Analyze Specification

Read SPEC.md thoroughly and identify:
- **Core functionality** - What the system must do
- **User interactions** - How users interact with the system
- **Data flows** - Information movement through the system
- **External integrations** - APIs, databases, services
- **Quality attributes** - Performance, security, scalability requirements

## Step 3: Define Root Node

The root node represents the entire system boundary. Determine:
- **Name**: Typically matches project name or system name
- **Responsibility**: High-level ownership of the entire system
- **Boundary**: What is inside vs. outside the system

## Step 4: Decompose to First Level

Identify 2-6 first-level components that:
- Are **cohesive** - Each has a single, clear responsibility
- Are **orthogonal** - Minimal overlap in concerns
- Cover all requirements - Every requirement maps to a component

### First-Level Component Patterns

| System Type | Common Components |
|-------------|-------------------|
| Web Application | UI Layer, API Layer, Data Layer |
| CLI Tool | CLI Parser, Core Engine, Output Formatter |
| Microservice | API Handler, Business Logic, Data Access |
| Library | Public API, Internal Core |

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

## Step 5: Verify Coverage

For each requirement in SPEC.md, verify:
- It maps to at least one node
- The node has clear responsibility for that requirement
- No requirement is orphaned or unaccounted for

Document any requirements that don't fit cleanly.

## Step 5.5: Clarify Dataflow

For each node, explicitly annotate inputs, outputs, and side-effects:

**Inputs:** What data/events the node consumes
- User interactions, API requests, file reads, database queries

**Outputs:** What the node produces
- Visual renders, API responses, file writes, data transformations

**Side-effects:** Changes to external state
- Database writes, network calls, state mutations, logging

**Common bidirectional patterns (do NOT force into acyclic structure):**
- UI: user events (input) ↔ visual updates (output)
- Library functions: arguments (input) ↔ return values (output)
- Event handlers: events (input) ↔ responses/side-effects (output)

## Step 6: Write ARCH_SUMMARY.md

Create `ARCH_SUMMARY.md` in the project root using the template:

```markdown
---
project: <Project Name>
version: 0.1.0
status: draft

tech_stack:
  language: <Language>
  framework: <Framework>
  test_framework: <Test Framework>
  runtime: <Runtime Model>

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

Status: stub
Doc: arch/<RootNodeName>.md

Responsibility:
<1-3 sentence high-level ownership description.>

Dataflow: (optional)
- Input: <what this node consumes>
- Output: <what this node produces>
- Side-effects: <external state changes, if any>

---

## <SubNode1>

Status: stub
Doc: arch/nodes/<SubNode1>.md

Responsibility:
<1-3 sentence summary of this node's purpose.>

Dataflow: (optional)
- Input: <what this node consumes>
- Output: <what this node produces>
- Side-effects: <external state changes, if any>

---

## <SubNode2>

Status: stub
Doc: arch/nodes/<SubNode2>.md

Responsibility:
<Short description.>

---
```

## Step 7: Generate Node Documentation

For each node, create a documentation file at `arch/nodes/<NodeName>.md`.

**Flexibility:** Depending on the project type and node responsibility, add or remove sections as appropriate. Not all sections (APIs, Events, Configuration) apply to every node.

```markdown
# <NodeName>

## Status

stub | partial | complete

## Responsibility

<1-2 paragraphs defining what this node owns and is accountable for. Include enough detail for future implementers to understand scope.>

## Dataflow

### Inputs

- <What data/events this node consumes>
- <e.g., user actions, API requests, file reads>

### Outputs

- <What this node produces>
- <e.g., visual renders, API responses, file writes>

### Side-effects

- <Changes to external state (database writes, network calls, logging)>
- <Leave blank if none>

## Public Interface

### Exposed APIs

- `functionName(param:): Type ReturnType` - <Brief purpose>

### Events Emitted

- `EventName` - <When emitted, what it contains>

### Configuration

- `configKey` - <Description, valid values, default>

## Dependencies

### Required

- `<DependencyName>` - <Why needed, interface used>

### Optional

- `<DependencyName>` - <Feature enabled when present>

## Invariants

- <Statement of truth that must always hold>
- <Another invariant>

## Status Rationale

<Why this node is stub/partial/complete>
```

## Constraints

### What This Skill Does NOT Do

- Deep internal design - Only define first-level structure
- Implementation details - No code, algorithms, or data structures
- Prioritization - Don't assign order to components
- Sequencing - Don't define implementation order
- Grandchildren - Never create nodes deeper than first level

### What Future Work Can Do

- Expand any node's subtree independently
- Add implementation details to node docs
- Create interfaces and contracts
- Define data models and schemas

## Success Criteria

- [ ] Root node represents complete system boundary
- [ ] First-level components are cohesive and orthogonal
- [ ] All requirements from SPEC.md map to nodes
- [ ] Structural dependencies form a tree (dataflow clarified separately)
- [ ] Bidirectional data flows documented (inputs/outputs/side-effects)
- [ ] ARCH_SUMMARY.md follows template exactly
- [ ] Each node has documentation file
- [ ] No implementation details in summary

## Next Steps

<!-- TODO: Chain into architecture review skill when available -->

After completing the architecture:
- If the architecture needs refinement - Re-run `root-architect`
- If ready to implement a node - Use subtree expansion workflow
- If architecture is complete - Proceed to implementation (future: arch-review skill)
