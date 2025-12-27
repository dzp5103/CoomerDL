# Quick Start Guide: Prompting AI Agents for CoomerDL Development

## 🚀 Quick Agent Prompting Cheat Sheet

### For Bug Fixes (15-30 min tasks)

```
@agent:clever-coder Fix BUG-001

Context: downloader/downloader.py line 227
Problem: Variable 'log_message' undefined when server returns 429
Expected: Define variable before use
Test: Download from rate-limited URL
```

**Even Simpler**:
```
Fix the undefined log_message bug in downloader.py safe_request() method
```

---

### For Performance Tasks (1-3 hours)

```
@agent:performance-optimizer Optimize PERF-001

Task: Database lookup performance
Current: 5.3s startup (loading 10k rows)
Target: <2s startup
Approach: Replace full cache with indexed queries
Validate: Measure before/after, ensure correctness
```

**Even Simpler**:
```
Profile and optimize the database loading in downloader.py - it's taking 5+ seconds on startup
```

---

### For New Features (2-8 hours)

```
@agent:clever-coder Implement FEATURE-001: Batch URL input

Requirements:
- Replace single-line URL entry with multi-line textbox
- Parse URLs (one per line)
- Validate each URL
- Download all valid URLs

Files: app/ui.py (entry widget around line 320)
Pattern: Use CTkTextbox like other multi-line inputs
Test: Paste 5 URLs, verify all download
```

**Even Simpler**:
```
Add support for multiple URLs in the input box - users should be able to paste several URLs (one per line) and download them all
```

---

### For Threading/Concurrency Issues

```
@agent:concurrency-expert Review thread safety in bunkr.py

Focus: Cancellation mechanism
Issue: Boolean flag causes race conditions
Solution: Replace with threading.Event()
Verify: Stress test with concurrent downloads + cancel
```

**Even Simpler**:
```
The cancel button doesn't always stop downloads in bunkr.py - fix the thread safety issue
```

---

## 📋 Template for Any Task

### Minimal Prompt (Just Get Started)
```
[Action] [What] in [Where]

Examples:
- Fix undefined variable in downloader.py
- Add caching to database lookups
- Optimize JPG5 download speed
- Refactor cancellation to use Events
```

### Good Prompt (Clear Requirements)
```
Task: [TASK-ID from ROADMAP]
File: [path/to/file.py]
Problem: [what's wrong or missing]
Goal: [what success looks like]
Test: [how to verify it works]
```

### Excellent Prompt (Complete Context)
```
Task: [TASK-ID] [Brief description]

Current Behavior:
[What happens now, with examples]

Expected Behavior:
[What should happen instead]

Implementation:
- Step 1: [specific change]
- Step 2: [specific change]
- Step 3: [specific change]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests pass

Files: [exact paths]
Constraints: [must maintain X, must not break Y]
```

---

## 🎯 Using Roadmap Tasks

### Method 1: Reference by ID
```
@agent:clever-coder Complete task BUG-002 from ROADMAP.md
```

The agent will:
1. Read ROADMAP.md
2. Find BUG-002 section
3. Extract FILE, PROBLEM, SOLUTION, DONE WHEN
4. Implement the fix
5. Run acceptance tests

### Method 2: Copy Task Details
```
From ROADMAP.md BUG-002:

Fix SimpCity missing base_url
File: downloader/simpcity.py
Problem: base_url referenced before assignment in process_page()
Solution: Set self.base_url in download_images_from_simpcity() before calling process_page()
```

### Method 3: Just Describe the Issue
```
SimpCity downloads are broken - there's a missing base_url variable somewhere in simpcity.py
```

---

## 💡 Pro Tips

### Tip 1: Agent Selection
- **Default (clever-coder)**: Bug fixes, features, general coding
- **performance-optimizer**: When task involves "slow", "optimize", "performance", "memory"
- **concurrency-expert**: When task involves "thread", "race", "lock", "deadlock", "cancel"

### Tip 2: Reference Documentation
```
@agent:clever-coder

Read the pattern in AI_AGENT_WORKFLOW.md "Pattern 1: Bug Fix"
Then fix BUG-003 in jpg5.py (unused import)
```

### Tip 3: Provide Examples
```
Add URL validation like this example:

def validate_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https')

Apply it to the URL input in app/ui.py
```

### Tip 4: Chain Multiple Steps
```
1. First fix BUG-001 (undefined log_message)
2. Then run the application to test
3. If working, move to BUG-002
4. Report progress after each bug
```

### Tip 5: Specify Testing
```
After implementing, test with:
1. python -c "from downloader.bunkr import BunkrDownloader; print('OK')"
2. python main.py
3. Paste a bunkr URL
4. Click download
5. Verify file appears in download folder
```

---

## 📚 Common Task Patterns from Roadmap

### Pattern: Fix Undefined Variable
```
File: [file.py]
Line: [line number]
Error: NameError: name 'variable' is not defined
Fix: Define 'variable' before line [line number]
```

### Pattern: Add Missing Import
```
File: [file.py]
Missing: import [module]
Reason: [class/function] requires [module]
```

### Pattern: Standardize Pattern
```
Files: [file1.py, file2.py, file3.py]
Current: [old pattern code]
New: [new pattern code]
Apply to all occurrences
```

### Pattern: Add New Feature
```
Feature: [name]
UI Changes: [describe widget changes]
Backend Changes: [describe logic]
Integration: [how it connects to existing code]
```

---

## 🔥 Quick Command Reference

### Browse Available Tasks
```
Show me all CRITICAL tasks from ROADMAP.md
```

### Get Task Details
```
What does task FEATURE-002 (BaseDownloader) require?
```

### Check Dependencies
```
What tasks must be completed before I can do FEATURE-003?
```

### Estimate Effort
```
How long will REFACTOR-001 take? What's the complexity?
```

### Get Code Context
```
Show me the current cancellation pattern in bunkr.py
```

---

## 🎬 Full Example: Start to Finish

### Step 1: Pick a Task
```
I want to work on performance optimization
```

### Step 2: Agent Responds
```
Based on ROADMAP_SUMMARY.md, here are the performance tasks:

🔴 PERF-001: Database indexing (15 min) 
🟠 PERF-002: Progress callback throttling (1 hour)
🟡 PERF-003: Connection pooling (30 min)

Which would you like to tackle first?
```

### Step 3: You Choose
```
Let's do PERF-001
```

### Step 4: Agent Executes
```
@agent:performance-optimizer

Reading PERF-001 from ROADMAP.md...
- File: downloader/downloader.py
- Problem: Full DB load on startup (50-100MB, 5.3s)
- Solution: Add index, use on-demand queries
- Expected: <2s startup, <10ms per query

Implementing...
[agent makes changes]

Testing...
✓ Baseline: 5.3s
✓ After: 0.9s (83% improvement)
✓ Downloads still work
✓ Duplicate detection functional

Complete! See commit abc1234.
```

---

## 📖 Learn More

- Full task list: `ROADMAP.md` or `ROADMAP_SUMMARY.md`
- Detailed specs: `TASKS.md` and `SPECIFICATIONS.md`
- Workflow patterns: `AI_AGENT_WORKFLOW.md`
- Agent details: `.github/agents/README.md`
- Common issues: `POTENTIAL_ISSUES.md`

---

## 🆘 Troubleshooting

### Agent Doesn't Understand
❌ "Make it faster"
✅ "Optimize the database loading in downloader.py - it takes 5 seconds"

### Agent Needs More Context
❌ "Fix the bug"
✅ "Fix the NameError in downloader.py line 227 where log_message is undefined"

### Agent Needs File Location
❌ "Add batch URL support"
✅ "Add batch URL support to the URL input widget in app/ui.py around line 320"

### Agent Needs Success Criteria
❌ "Improve performance"
✅ "Reduce startup time from 5s to under 2s by optimizing database loading"

---

## 🎯 Bottom Line

**Simplest Possible Prompt**:
```
[Do what] to [specific thing] in [exact file]
```

**Example**:
```
Add an index to the media_url column in the downloads table in downloader.py
```

That's it! The agent will figure out the details from the documentation you've already created.
