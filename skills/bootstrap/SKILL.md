---
name: bootstrap
description: "Bootstraps new projects with appropriate tech stack selection. Use when user wants to start a new project and needs help choosing and initializing the tech stack."
argument-hint: "[project description or tech stack]"
---

# Project Bootstrap

## Overview

Help users bootstrap new projects by recommending appropriate tech stacks and creating a minimal hello-world project that compiles and runs. This skill bridges the gap between specification (from specify skill) and implementation.

**User's Intent:** $ARGUMENTS

## Workflow

Follow this process in order:

1. **Check specification** - Verify SPEC.md exists and has no critical ambiguities
2. **Understand the project** - Read SPEC.md and README.md to understand what the project should do
3. **Evaluate user tech stack preference** - If user provided a tech stack argument, evaluate it
4. **Propose tech stack options** - Present 2-3 options with pros/cons and recommendations
5. **Document tech stack choice** - Record the selected stack in SPEC.md
6. **Create minimal project** - Initialize a hello-world level project that compiles/runs with passing tests
7. **Verify it works** - Ensure the project runs and tests pass

## Step 1: Check Specification

**STOP CONDITION: Do not proceed without a valid specification.**

1. Check if SPEC.md exists in the project root
2. If SPEC.md does NOT exist:
   - Stop immediately
   - Invoke the `specify` skill to create a specification
   - Tell the user: "A specification is required before bootstrapping. Running specify skill..."
3. If SPEC.md exists but contains `[NEEDS CLARIFICATION]` markers:
   - These are critical ambiguities that affect tech stack choice
   - Stop immediately
   - Invoke the `specify` skill to resolve them
   - Tell the user: "The specification has unresolved questions that affect tech stack choice. Running specify skill..."

## Step 2: Understand the Project

Read SPEC.md to understand:
- What the project does
- Target users
- Platform requirements (web, desktop, mobile, CLI)
- Performance constraints
- Integration needs

Also check README.md for any existing architectural decisions or technology preferences.

## Step 3: Evaluate User Tech Stack Preference

**If user provided a tech stack argument (e.g., "/bootstrap Python" or "/bootstrap React + Node.js"):**

1. **Accept it as a strong preference** unless:
   - It clearly doesn't fit the project requirements
   - There's an objectively better solution for the use case

2. **If rejecting, state clearly why:**
   - "That stack won't work because..." or "For this use case, X is better because..."
   - Present specific alternatives with reasoning
   - Ask user to choose again

3. **If user insists, accept their choice:**
   - Move forward with user's preference
   - Do your best to make it work

## Step 4: Propose Tech Stack Options

Present 2-3 options with clear reasoning. Rely on your knowledge of tech stacks - do not use a fixed reference table as project types vary widely (games, desktop apps, mobile apps, static sites, APIs, etc. all have different appropriate stacks).

### For Each Option, Include:

- **Language/Framework**: What and why
- **Testing Framework**: Test runner and assertion library (crucial for automated testing)
- **Pros**: Key advantages (ecosystem, performance, learning curve, testing support)
- **Cons**: Key drawbacks
- **Best for**: Ideal use cases
- **Recommendation**: Strong/Moderate/Use case specific

### Testability Considerations

When evaluating tech stacks, prioritize testability:

- **Test framework availability**: Are there mature, widely-used testing frameworks?
- **Test isolation**: Can tests run independently without external dependencies?
- **Mocking support**: Are there good libraries for mocking/stubbing?
- **Fast feedback**: Can tests run quickly for rapid iteration?
- **CI integration**: Does the framework integrate easily with CI pipelines?

A tech stack with excellent testing support enables:
- Reliable automated testing throughout development
- Confidence when refactoring
- Regression prevention
- TDD workflow support (red→green→refactor)

### Example Presentation

```
Based on your project (REST API with JSON), here are my recommendations:

1. **Python + FastAPI** (Recommended)
   - Testing Framework: pytest
   - Pros: Fast development, automatic docs, type validation, pytest excellent for testing
   - Cons: Slower than compiled languages
   - Best for: APIs, microservices

2. **Node.js + Express**
   - Testing Framework: Jest
   - Pros: Huge ecosystem, JavaScript everywhere, Jest is mature and widely-used
   - Cons: Callback hell (mitigated with async/await)
   - Best for: Full-stack JS projects

3. **Go + Gin**
   - Testing Framework: Go's built-in testing package
   - Pros: Fast, simple, great for concurrency, testing included in stdlib
   - Cons: Less expressive, verbose boilerplate
   - Best for: High-performance APIs
```

## Step 5: Document Tech Stack Choice

After the user selects a tech stack from Step 4, **update SPEC.md** to record the choice:

1. Add or update a "Tech Stack" section in SPEC.md
2. Include:
   - Language and framework
   - Key dependencies
   - Reasoning for the choice (brief)

Example:
```markdown
## Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Testing Framework**: pytest
- **Reasoning**: Fast development, automatic OpenAPI docs, type validation, pytest provides excellent testing with fixtures and parametrization
```

**Note:** Always include the testing framework in the tech stack documentation. This is essential for TDD workflow and automated testing.

## Step 6: Create Minimal Project

**CRITICAL: Keep it minimal. The project must:**
- Be hello-world level (print "Hello, World!" or equivalent)
- Compile without errors
- Run without errors
- Include a minimal passing test
- NOT reflect any system architecture

### Project Structure (Minimal)

```
project-root/
├── src/                 # or app/, lib/ - keep minimal
│   └── main.{ext}      # entry point (py, js, go, rs, etc.)
├── tests/              # Test directory (or test/, __tests__/, spec/)
│   └── main_test.{ext} # Minimal passing test
├── package.json         # or requirements.txt, go.mod, etc.
├── pyproject.toml       # or setup.cfg, package.json with test config
└── README.md           # basic instructions
```

### Technology-Specific Templates

**Python:**
```python
# src/main.py
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

**Node.js:**
```javascript
// src/index.js
console.log("Hello, World!");
```

**Go:**
```go
// src/main.go
package main

func main() {
    println("Hello, World!")
}
```

**Rust:**
```rust
// src/main.rs
fn main() {
    println!("Hello, World!");
}
```

**TypeScript/React:**
```typescript
// src/App.tsx
export default function App() {
  return <h1>Hello, World!</h1>;
}
```

### Test Setup by Language

Add a minimal passing test for each language:

**Python (pytest):**
```python
# tests/test_main.py
def test_placeholder():
    """Placeholder test - replace with real tests during implementation."""
    assert True
```

**Node.js/JavaScript (Jest):**
```javascript
// tests/main.test.js
describe('placeholder', () => {
  test('placeholder test', () => {
    expect(true).toBe(true);
  });
});
```

**Go (testing):**
```go
// main_test.go
package main

import "testing"

func TestPlaceholder(t *testing.T) {
    // Placeholder test - replace with real tests during implementation
    t.Log("Placeholder test passes")
}
```

**Rust (built-in):**
```rust
// src/main.rs (or tests/integration_test.rs)
#[test]
fn placeholder() {
    // Placeholder test - replace with real tests during implementation
    assert!(true);
}
```

**TypeScript/Jest:**
```typescript
// tests/main.test.ts
describe('placeholder', () => {
  test('placeholder test', () => {
    expect(true).toBe(true);
  });
});
```

## Step 7: Verify It Works

After creating the project:

1. **Install dependencies** - Run package manager install
2. **Run the project** - Execute the entry point
3. **Confirm output** - Verify "Hello, World!" or equivalent appears
4. **Run tests** - Execute the test suite
5. **Confirm tests pass** - Verify all tests pass (including the placeholder test)

**Critical:** Both the project running AND tests passing are required for successful bootstrap.

Report success:
```
✅ Project bootstrapped successfully!
- Tech stack: [chosen stack]
- Testing framework: [test framework]
- Project location: [path]
- Run command: [how to run]
- Test command: [how to run tests]
```

## Key Principles

- **User choice first** - Respect user's tech stack preference unless clearly wrong
- **Minimal to start** - Don't add complexity until needed
- **Working baseline** - Always verify the project compiles/runs and tests pass before concluding
- **Clear recommendations** - Help users understand trade-offs
- **Testability first** - Always include testing framework in tech stack decisions; a project without tests is not production-ready

## Next Steps

After bootstrapping the project:

### On Success
- The project compiles and runs without errors
- The placeholder test passes
- **Action:** Invoke the `plan-milestones` skill to plan implementation milestones, then `arch-init` to define the system architecture

### On Failure
- **Logic bugs or syntax errors:**
  - Fix the issue directly in the created project files
  - Re-run verification until the project works AND tests pass
  - Do not proceed to architecture until the baseline is functional
- **Test failures:**
  - Fix the test configuration (test runner, test discovery patterns)
  - Ensure test dependencies are properly installed
  - Tests must pass before proceeding to architecture
- **Environment issues (missing tools/packages):**
  - Provide clear guidance to the user on what's needed
  - Example: "Please install Node.js 18+ from https://nodejs.org" or "Run `pip install -r requirements.txt`"
  - Ask the user to install the required tools and re-run the skill
