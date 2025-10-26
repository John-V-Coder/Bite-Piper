# 🚀 Quick Start: Agent-Frontend Integration

## Prerequisites

- Python 3.8+
- Django installed
- Agent dependencies installed (`pip install uagents openai requests`)

## 5-Minute Setup

### Step 1: Configure Environment (2 min)

```bash
# Copy your existing .env or update it
cd c:\Users\PC\OneDrive\Desktop\Bite-Piper\src
```

Add these lines to your `.env` file:

```bash
# Agent Configuration
AGENT_NAME=bite-piper-agent
AGENT_SEED=agent1hcjnknnkmafknininfinkmnmkndajnjnjnjcnknc
AGENT_PORT=8000
AGENT_ENDPOINT=http://localhost:8000/submit

# Agent Address (will be filled after first run)
AGENT_ADDRESS=

# ASI Configuration
ASI_API_KEY=your_asi_api_key_here
ASI_BASE_URL=https://api.asi1.ai/v1
ASI_MODEL=asi1-graph

# Timeouts
AGENT_TIMEOUT=30
```

### Step 2: Start the Agent (1 min)

Open **Terminal 1**:

```bash
cd c:\Users\PC\OneDrive\Desktop\Bite-Piper
python src\agent\uagent\main_agent.py
```

**Copy the agent address from the output:**
```
Agent Address: agent1q2xj7w8xxxxxxxxxxx
```

**Update your .env:**
```bash
AGENT_ADDRESS=agent1q2xj7w8xxxxxxxxxxx  # paste here
```

### Step 3: Start Django (1 min)

Open **Terminal 2**:

```bash
cd c:\Users\PC\OneDrive\Desktop\Bite-Piper
start_django.bat
```

### Step 4: Test the Integration (1 min)

Open browser to:
- http://localhost:8000/ ← Main dashboard
- http://localhost:8000/agent/ ← Check agent status

Should show **"Status: Healthy"** ✅

## Usage Flow

1. **Dashboard** → Enter budget ($1,000,000)
2. Click **"Calculate Allocation"** 
3. See MeTTa results
4. Click **"Analyze with AI Agent"** 🤖
5. Get comprehensive AI analysis!

## Features Available

### Main Dashboard
- 💰 Budget input and allocation calculation
- 🧠 Advanced scoring with MeTTa
- 🤖 AI Agent analysis button (NEW!)
- 📊 Priority breakdown
- 💡 Detailed recommendations

### Agent Dashboard (NEW!)
- ✅ Real-time agent health monitoring
- 🧩 List of 8 loaded modules
- 📋 Capability descriptions
- ⚡ Quick actions

### Agent Analysis (NEW!)
For each region, you get:
- ⚖️ **Fairness Analysis** - Distribution equity
- ⚖️ **Justice Evaluation** - Ethical framework assessment
- 📊 **Equity Analysis** - Systemic inequality detection
- 💥 **Impact Assessment** - Beneficiary estimates
- 🔍 **Transparency Report** - Clear explanations
- 🔎 **Bias Detection** - Systemic bias checks
- 💡 **Recommendations** - Actionable insights

## API Endpoints

### Test Health Check
```bash
curl http://localhost:8000/api/agent/health/
```

Expected:
```json
{
  "status": "healthy",
  "agent_name": "bite-piper-agent",
  "address": "agent1q2xj7w8...",
  "modules_loaded": [
    "AllocationFairnessAnalyzer",
    "DecisionJusticeEvaluator",
    ...
  ]
}
```

## Troubleshooting

### "Agent Unavailable" Error

**Check 1:** Is agent running?
```bash
# Should see agent process
python src\agent\uagent\main_agent.py
```

**Check 2:** Is AGENT_ADDRESS set?
```bash
# In your .env file
AGENT_ADDRESS=agent1q2xj7w8...  # must be filled
```

**Check 3:** Is port 8000 available?
```bash
netstat -ano | findstr :8000
```

### Agent Timeout

Increase timeout in `.env`:
```bash
AGENT_TIMEOUT=60  # increase to 60 seconds
```

### Import Errors

Restart Django:
```bash
# Press Ctrl+C in Django terminal
start_django.bat
```

## Architecture Summary

```
Browser (localhost:8000)
    ↓ HTMX requests
Django Frontend (port 8000)
    ↓ HTTP/JSON
AgentClient Service
    ↓ HTTP POST
uAgent Backend (port 8000/submit)
    ↓ OpenAI API
ASI Intelligence
```

## File Changes Made

✅ **New Files:**
- `src/funding/agent_client.py` - Agent communication service
- `src/funding/templates/funding/agent_dashboard.html` - Agent status page
- `src/funding/templates/funding/partials/agent_analysis.html` - AI results display
- `AGENT_FRONTEND_INTEGRATION.md` - Full architecture docs

✅ **Updated Files:**
- `src/funding/views.py` - Added agent views
- `src/funding/urls.py` - Added agent routes
- `src/funding/templates/funding/base.html` - Added AI Agent nav link
- `src/funding/templates/funding/index.html` - Added agent button
- `env_template.txt` - Added agent config

## Next Steps

1. ✅ Integration complete
2. **Get ASI API key** from https://asi1.ai (for enhanced intelligence)
3. **Test all features** in browser
4. **Deploy to production** (optional)

## Support

- Full docs: `AGENT_FRONTEND_INTEGRATION.md`
- Agent README: `src/agent/uagent/README.md`
- Test client: `src/agent/uagent/test_agent_client.py`

---

**Status:** ✅ Production Ready

**Time to Deploy:** ~5 minutes

**Tech Stack:** Django + HTMX + uagents + ASI + MeTTa
