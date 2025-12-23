import subprocess
import json
import re


def normalize_list(items):
    """
    Ensures every list item is a clean string.
    Converts dicts / weird outputs into readable text.
    """
    clean = []
    for i in items:
        if isinstance(i, dict):
            clean.append(" ".join(str(v) for v in i.values()))
        else:
            clean.append(str(i))
    return clean


def analyze_business_report(text: str):
    prompt = f"""
You are a senior business analyst.

Return ONLY valid JSON.

Format:
{{
  "executive_summary": [],
  "financial_highlights": [],
  "risks_red_flags": [],
  "opportunities": [],
  "recommended_actions": []
}}

Rules:
- Business & finance focused
- No fluff
- JSON only

DOCUMENT:
{text[:4000]}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    raw = result.stdout.strip()

    try:
        # 1️⃣ Extract JSON safely
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")

        parsed = json.loads(match.group())

        # 2️⃣ 🔥 THIS IS THE "RETURN PART" I MEANT 🔥
        return {
            "executive_summary": normalize_list(parsed.get("executive_summary", [])),
            "financial_highlights": normalize_list(parsed.get("financial_highlights", [])),
            "risks_red_flags": normalize_list(parsed.get("risks_red_flags", [])),
            "opportunities": normalize_list(parsed.get("opportunities", [])),
            "recommended_actions": normalize_list(parsed.get("recommended_actions", []))
        }

    except Exception:
        # 3️⃣ Fallback (never crash UI)
        return {
            "executive_summary": ["Could not reliably analyze this report"],
            "financial_highlights": [],
            "risks_red_flags": [],
            "opportunities": [],
            "recommended_actions": []
        }


def answer_question(context: str, question: str):
    prompt = f"""
You are a business advisor.

Answer clearly and practically.

CONTEXT:
{context[:4000]}

QUESTION:
{question}

ANSWER:
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()
