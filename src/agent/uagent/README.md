# 🏛️ Bite-Piper uAgent - Civic Decision-Making AI

## Overview

Bite-Piper is an intelligent autonomous agent for civic decision-making that integrates:
- **11 Philosophical Frameworks** (Rawls, Sen, Aristotle, Foucault, Freire, hooks, Young, Fanon, Butler, Ostrom, Nussbaum)
- **Real-World Civic Data** (World Bank, Census Bureau, Open Government APIs)
- **ASI Intelligence** for enhanced strategic insights
- **Full Transparency & Explainability**

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install uagents python-dotenv openai requests
```

### 2. Configure Environment

Copy `env_template.txt` to `.env` and fill in your API keys:

```bash
cp ../../env_template.txt ../../.env
```

Required configuration:
- `AGENT_NAME`: Your agent's name
- `AGENT_SEED`: Secret seed phrase (keep secure!)
- `AGENT_PORT`: Port to run agent (default: 8000)
- `ASI_API_KEY`: Your ASI API key from https://asi1.ai
- `CENSUS_API_KEY`: US Census API key from https://api.census.gov/data/key_signup.html

### 3. Start the Agent

```bash
python main_agent.py
```

You'll see:
```
🏛️  BITE-PIPER - Civic Decision-Making AI Agent
=================================================================
Starting agent 'bite-piper-agent' on port 8000...
Endpoint: http://localhost:8000/submit
=================================================================

Agent Name: bite-piper-agent
Agent Address: agent1q2xj7w8... (save this!)
```

**IMPORTANT:** Copy the agent address shown in the logs - you'll need it for testing!

### 4. Test the Agent

Update `test_agent_client.py` with your agent's address:

```python
BITE_PIPER_AGENT_ADDRESS = "agent1q2xj7w8..."  # Your agent's address
```

Then run:

```bash
python test_agent_client.py
```

## 📋 Agent Capabilities

### 1. **Allocation Fairness Analysis**
- Rawlsian difference principle
- Sen's capability approach
- Aristotelian golden mean
- Gini coefficient calculation

### 2. **Decision Justice Evaluation (4 Dimensions)**
- Distributive Justice
- Procedural Justice
- Recognitional Justice
- Restorative Justice

### 3. **Equity Impact Analysis (6 Dimensions)**
- Economic equity
- Educational equity
- Health equity
- Geographic equity
- Demographic equity
- Intersectional equity

### 4. **Cross-Demographic Impact Assessment**
- Low-income populations
- Rural vs Urban
- Women, Youth, Elderly
- Intersectional impacts (hooks' framework)

### 5. **Systemic Bias Detection**
- Young's five faces of oppression
- Socioeconomic bias
- Geographic bias
- Intersectional bias (hooks)

### 6. **Policy Discourse Analysis**
- Foucauldian power analysis
- Deficit framing detection
- Paternalistic language detection

### 7. **Stakeholder Mediation**
- Young's communicative democracy
- Freire's problem-posing dialogue
- Ostrom's polycentric governance
- Power imbalance detection

### 8. **Transparency & Explainability**
- Decision rationale
- Data provenance
- Philosophical justification
- Alternative scenarios
- Export to JSON, Markdown, HTML

## 🎯 Usage Examples

### Example 1: Analyze Resource Allocation

```python
from main_agent import DecisionRequest
from uagents.query import query

decision = DecisionRequest(
    decision_id="ALLOC-2025-001",
    decision_type="allocation",
    decision_data={
        "total_budget": 10000000,
        "allocations": {
            "region_A": 4000000,
            "region_B": 3000000,
            "region_C": 2000000,
            "region_D": 1000000
        },
        "needs_data": {
            "region_A": {"poverty_rate": 0.6, "literacy_rate": 0.5},
            "region_B": {"poverty_rate": 0.4, "literacy_rate": 0.7},
            # ... more regions
        }
    },
    regions=[
        {"id": "region_A", "type": "country", "code": "REG-A"},
        # ... more regions
    ],
    explanation_depth="full"
)

response = await query(
    destination="agent1q...",  # Your agent address
    message=decision,
    timeout=60.0
)

print(response.recommendations)
```

### Example 2: Mediate Stakeholder Conflicts

```python
decision = DecisionRequest(
    decision_id="MEDIATE-2025-001",
    decision_type="stakeholder_mediation",
    decision_data={...},
    regions=[...],
    stakeholders=[
        {
            "id": "community_leaders",
            "type": "community",
            "interests": ["equitable distribution"],
            "concerns": ["urban bias"]
        },
        {
            "id": "government",
            "type": "government",
            "interests": ["efficiency"],
            "concerns": ["budget constraints"]
        }
    ]
)
```

## 📊 Response Structure

```json
{
  "decision_id": "ALLOC-2025-001",
  "timestamp": "2025-10-26T21:00:00",
  "analysis": {
    "fairness": {...},
    "justice": {...},
    "equity": {...},
    "impact": {...},
    "bias": {...},
    "stakeholder_mediation": {...}
  },
  "recommendations": [
    {
      "source": "equity_analysis",
      "recommendation": "Address 5 economic equity disparities",
      "priority": "high",
      "strategies": [...]
    }
  ],
  "transparency_report": {
    "decision_rationale": {...},
    "data_provenance": {...},
    "philosophical_justification": {...},
    "alternative_scenarios": {...}
  },
  "asi_insights": "Strategic recommendations from ASI..."
}
```

## 🔐 Security Notes

1. **Never commit `.env` file** - It contains sensitive API keys
2. **Keep AGENT_SEED secure** - It generates your agent's address
3. **Use HTTPS endpoints** in production
4. **Rotate API keys** regularly

## 📚 Philosophical Frameworks Used

- **Rawls**: Justice as fairness, difference principle
- **Sen**: Capability approach, substantive freedoms
- **Aristotle**: Virtue ethics, golden mean
- **Foucault**: Power/knowledge, discourse analysis
- **Freire**: Critical pedagogy, conscientization
- **hooks**: Intersectionality, matrix of domination
- **Young**: Communicative democracy, structural injustice
- **Fanon**: Decolonial theory, reparative justice
- **Butler**: Recognition ethics, precarity
- **Ostrom**: Polycentric governance, commons management
- **Nussbaum**: Central capabilities list

## 🛠️ Troubleshooting

### Agent won't start
- Check port 8000 is available
- Verify `.env` file exists and is properly formatted
- Check Python version (requires 3.8+)

### ASI insights not working
- Verify `ASI_API_KEY` is set in `.env`
- Check ASI API quota
- Agent will still work without ASI

### Census data unavailable
- Register for Census API key
- Update `CENSUS_API_KEY` in `.env`
- Agent uses World Bank data as fallback

## 📞 Support

For issues or questions:
- GitHub Issues: [Your repo]
- Documentation: [Your docs]
- Email: [Your email]

## 📄 License

[Your License]

---

**Built with ❤️ for civic justice and equity**
