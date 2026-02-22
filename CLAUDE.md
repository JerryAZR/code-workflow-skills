# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **arch-kit** - a collection of Claude Code skills that implement a two-tier architectural model

## Architecture Structure

- `.claude-plugin/` - Claude Code plugin containing skills and commands
- `scripts/` - Utility scripts (security scanning)

## Commands

### Security Scanning
```bash
uv run scripts/security_scan_all.py
```

### Running Skills (via plugin)
After installing the plugin, skills are invoked via `/arch-kit:skill-name`:
```bash
/arch-kit:spec-create "project description"
/arch-kit:spec-clarify
/arch-kit:project-init
/arch-kit:milestone-plan-all
/arch-kit:arch-init
/arch-kit:arch-decompose
/arch-kit:milestone-init
/arch-kit:node-prep
/arch-kit:node-build
/arch-kit:milestone-test-add
/arch-kit:milestone-integrate
/arch-kit:milestone-wrapup
/arch-kit:issue-create "feature or bug"
/arch-kit:issue-plan <issue-id>
/arch-kit:issue-resolve <issue-id>
/arch-kit:quick-patch "fix description"
```

### Testing Plugin
```bash
# Validate plugin
claude plugin validate ./

# Load local plugin for testing
claude --plugin-dir .claude-plugin
```

## Key Concepts

### Two-Tier Workflow
- **Outer Tier (Rare, Structural)**: Architecture decisions made infrequently
- **Inner Tier (Frequent, Local)**: Test-driven implementation of individual components

### Node State Model
Architecture nodes progress through states: `pending` → `atomic`/`decomposed` → `planned` → `prepared` → `implemented` → `modified`

### Core Principles
- **Stable topology, evolving contract** - Architecture tree is fully elaborated early and remains fixed; milestones expand what each node must provide
- **One-level decomposition** - Only decompose one level at a time to prevent context explosion
- **TDD enforced** - Tests must fail before implementation; never weaken tests to make them pass
- **Bounded scope** - Each iteration is small, local, and context-efficient

### Key Files
- `arch/ARCH_SUMMARY.md` - Architecture documentation with node states
- `SPEC.md` - Project specifications
- `tests/<node_path>.py` - Test files (e.g., `tests/auth/test_user_validator.py`)
- `src/<node_path>.py` - Implementation files

### Skill Dependencies
- `node-build` requires `node-prep` to be run first
- `milestone-wrapup` should be run after all nodes in a milestone are implemented
- Skills follow a strict order in the workflow chain

## Workflow Chains

**Setup**: spec-create → spec-clarify → project-init → milestone-plan-all

**Architecture**: arch-init → arch-decompose (repeat until tree complete)

**Implementation**: milestone-init → node-prep → node-build (repeat) → milestone-test-add → milestone-integrate → milestone-wrapup

**Issue Management**: issue-create → issue-plan → issue-resolve
