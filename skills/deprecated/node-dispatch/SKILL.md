---
name: node-dispatch
description: "DEPRECATED: Use node-decompose directly. This skill selected and deferred nodes, but the new approach uses stable topology with behavioral scope gating."
argument-hint: "[node-name or priority-focus]"
---

# Node Dispatch

> **DEPRECATED** - This skill is no longer used. The new workflow uses stable topology where all nodes are elaborated from the start. Use `node-decompose` directly instead.

## Overview

Coordinate milestone progress with architecture decomposition by selecting the next pending node relevant to the current milestone and dispatching to `node-decompose` for decomposition.

This skill bridges MILESTONES.md (feature-focused) with ARCH_SUMMARY.md (architecture-focused) by:
1. Identifying the current milestone from MILESTONES.md
2. Finding pending nodes in ARCH_SUMMARY.md
3. Determining which pending node is most relevant to the current milestone
4. Dispatching to node-decompose for that node
5. Marking irrelevant nodes as "deferred" when clearly not related

**User's Intent:** $ARGUMENTS

**Argument Handling:** If the user provides a node-name (e.g., "AuthNode"), verify it exists in ARCH_SUMMARY.md with "pending" status. If it exists but is deferred, mark it back to "pending" to honor the user's priority.

If the user provides a priority focus (e.g., "API focus" or "MVP first"), treat it as a hint for which node to decompose next. Respect if it makes sense, even if the node relates to a future milestone. Argue against if it requires foundational work that far exceeds current milestone scope. If the user insists, try your best to make it work.

## Prerequisites

- `MILESTONES.md` exists in project root
- `arch/ARCH_SUMMARY.md` exists with pending nodes
- Run `arch-init` first if architecture doesn't exist

## Workflow

Follow this process in order:

1. **Read Current Milestone** - Identify the active milestone from MILESTONES.md
2. **Find Pending Nodes** - Locate all pending nodes in ARCH_SUMMARY.md
3. **Assess Relevance** - Determine if each pending node relates to current milestone
4. **Decide: Decompose or Defer** - Take action on the target node
5. **Dispatch** - Invoke node-decompose on the selected node

---

## Step 1: Read Current Milestone

Read `MILESTONES.md` to identify the current active milestone:

1. Find the first milestone with status "in-progress" or "planned" (if no in-progress)
2. Extract the milestone name and its features
3. Understand what the milestone aims to achieve

**Error Handling:**
- If `MILESTONES.md` does not exist, inform the user: "No MILESTONES.md found. Run `plan-milestones` first to create the milestone plan."
- If `MILESTONES.md` exists but no milestone has status "in-progress" or "planned", report completion or ask user to activate a milestone.

---

## Step 2: Find Pending Nodes

Read `arch/ARCH_SUMMARY.md` to locate all pending nodes:

1. Search for all nodes with "Status: pending"
2. Note each node's responsibility and dataflow
3. Collect the full list of pending nodes

**Error Handling:**
- If `arch/ARCH_SUMMARY.md` does not exist, inform the user: "No architecture found. Run `arch-init` first to initialize the architecture."
- If ARCH_SUMMARY.md exists but has no nodes with "Status: pending", proceed to Step 3 with an empty list.

**If no pending nodes exist:**
- No pending nodes → Architecture decomposition complete (deferred nodes remain deferred, atomic nodes are done)
- If all nodes are implemented → Project complete
- Report the status to user

---

## Step 3: Assess Relevance

For each pending node, determine if it relates to the current milestone:

**Related if the node's responsibility:**
- Supports one or more features in the current milestone
- Is a prerequisite for milestone features
- Is part of the core infrastructure needed now

**Clearly Deferred (mark deferred) if:**
- The node is for a feature in a future milestone
- The node is for a "could-have" or "future" feature
- The node is unrelated to any current milestone features

**When unsure → Decompose** - Better to decompose and refine later than to defer incorrectly.

### Decision Table

| Scenario | Action |
|----------|--------|
| Node clearly related to current milestone | Decompose |
| Node clearly for future milestone | Defer |
| Unsure if related | Decompose |
| No pending nodes | Report completion |

---

## Step 4: Decide - Decompose or Defer

Based on the relevance assessment:

### If Decompose

Select the most relevant pending node:
- Prefer nodes that directly support current milestone features
- If multiple candidates, pick the one most central to the milestone
- If user provided a node-name argument, verify it exists and is pending

### If Defer

Update the node status in `arch/ARCH_SUMMARY.md`:
1. Change "Status: pending" to "Status: deferred"
2. Add a brief note: "Deferred to: <future milestone or reason>"
3. Move to the next pending node and reassess

---

## Step 5: Dispatch to Node-Decompose

Invoke the `node-decompose` skill on the selected node:

```
node-decompose <node-name>
```

If no node-name provided to this skill, use the node selected in Step 4.

After node-decompose completes:
- Check if there are more pending nodes
- Re-run this skill to continue with the next node
- Or report completion if no pending nodes remain

---

## Constraints

### What This Skill Does NOT Do

- Modify MILESTONES.md - Only reads to understand context
- Implement nodes - Dispatches to node-decompose for that
- Guess incorrectly - When unsure, always decomposes rather than defers
- Handle implementation - Use `node-prep` and `node-build` for that

---

## Success Criteria

- [ ] Current milestone identified from MILESTONES.md
- [ ] All pending nodes found in ARCH_SUMMARY.md
- [ ] Relevance assessed for each pending node
- [ ] Clearly irrelevant nodes marked as "deferred"
- [ ] Relevant node dispatched to node-decompose
- [ ] Progress reported to user

## Next Steps

After node-decompose completes:
- **Continue dispatching**: Re-run `node-dispatch` to handle the next pending node
- **Check milestone progress**: If current milestone features are covered, move to next milestone
- **Implementation phase**: When all architecture nodes are decomposed, run `node-prep` to prepare nodes for implementation
