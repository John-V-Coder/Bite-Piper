#!/usr/bin/env python3
"""
metta_company_policy_json.py

Full example: Convert company metrics to MeTTa facts, define symbolic rules,
and query with ChatGPT using MeTTa-Motto streaming with JSON output.
"""

from motto.agents import MettaAgent
import json
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv  # 👈 add this
# Load .env file
load_dotenv()

# Get the key from .env
api_key = os.getenv("OPENAI_API_KEY")

# Ensure it exists
if not api_key:
    raise EnvironmentError("⚠️ OPENAI_API_KEY not found in .env file. Please check your setup.")

# Set it for all libraries that expect it in the environment
os.environ["OPENAI_API_KEY"] = api_key
# -----------------------------
# Helper: Convert JSON / CSV to MeTTa facts
# -----------------------------
def json_to_facts(data, parent_key=""):
    facts = []

    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            facts.extend(json_to_facts(v, full_key))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            full_key = f"{parent_key}[{i}]"
            facts.extend(json_to_facts(item, full_key))
    else:
        key_clean = parent_key.replace(" ", "_").replace("-", "_")
        if isinstance(data, str):
            facts.append(f'(Fact "{key_clean}" "{data}")')
        else:
            facts.append(f'(Fact "{key_clean}" {data})')
    return facts


# -----------------------------
# Load company data (robust path)
# -----------------------------
possible_paths = [
    Path(__file__).parent / "socioeconomic_supply_chain_data.json",
    Path(__file__).parent.parent / "socioeconomic_supply_chain_data.json"
]

company_data_path = None
for p in possible_paths:
    if p.exists():
        company_data_path = p
        break

if not company_data_path:
    raise FileNotFoundError(
        "Cannot find 'socioeconomic_supply_chain_data.json' in current or parent folder."
    )

# Load JSON or Excel/CSV
if company_data_path.suffix.lower() == ".json":
    with open(company_data_path, "r") as f:
        company_data = json.load(f)
elif company_data_path.suffix.lower() in [".xls", ".xlsx", ".csv"]:
    xls = pd.ExcelFile(company_data_path)
    company_data = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)
        company_data[sheet_name] = df.to_dict(orient="records")
else:
    raise ValueError("Unsupported file type")

facts_list = json_to_facts(company_data)
media_msg = "\n".join(facts_list)


# -----------------------------
# Define MeTTa rules for reasoning
# -----------------------------
rules_code = '''
; Detect high expense departments
(= (high_expense_department $dep)
   (case (match &self (Fact $key $val))
       (($key (contains-str $key "expenses"))
        (if (> $val 100000) $key False))))

; Detect low revenue departments
(= (low_revenue_department $dep)
   (case (match &self (Fact $key $val))
       (($key (contains-str $key "revenue"))
        (if (< $val 50000) $key False))))

; Generate JSON structured policy recommendations
(= (policy_recommendation_json)
   (concat-str "{\\"high_expense_departments\\":["
       (high_expense_department)
       "], \\"low_revenue_departments\\":["
       (low_revenue_department)
       "]}"
   )
)
'''


# -----------------------------
# Combine facts + rules for agent
# -----------------------------
agent_code = f'''
{rules_code}

(= (respond)
   ((chat-gpt-agent (model_name) (is_stream) True)
      (Messages
         (system (system_msg))
         (media (media_msg))
         (user (messages))
      )
   )
)
(= (response) (respond))
'''

# -----------------------------
# Initialize MeTTa agent
# -----------------------------
agent = MettaAgent(code=agent_code)


# -----------------------------
# System message
# -----------------------------
system_msg = """
You are an AI assistant for internal company policy and governance analysis.
Use ONLY the provided company facts.
Provide policy recommendations in JSON format with keys:
  - high_expense_departments
  - low_revenue_departments
Return JSON ONLY, no extra text.
"""


# -----------------------------
# User query
# -----------------------------
query = "Generate structured JSON governance and policy recommendations."

response_stream = agent(
    f'(user "{query}")',
    additional_info=[
        ("system_msg", system_msg, 'String'),
        ("media_msg", media_msg, 'String'),
        ("model_name", "gpt-4o", 'String'),
        ("is_stream", True, 'Bool')
    ]
).content


# -----------------------------
# Streamed output (Fixed)
# -----------------------------
print("\n--- JSON Response ---\n")
json_output = ""

for chunk in response_stream:
    # Convert symbolic output to text safely
    json_output += str(chunk)

# Parse to ensure valid JSON
try:
    structured_output = json.loads(json_output)
    print(json.dumps(structured_output, indent=2))
except json.JSONDecodeError:
    print("Error: Response is not valid JSON. Raw output below:\n")
    print(json_output)

print("\n--- End of Response ---\n")
