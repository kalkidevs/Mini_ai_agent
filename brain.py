import os
import json
from openai import OpenAI

ICP = "High-end bespoke WordPress/Headless CMS development projects requiring integration with an external CRM, with a stated budget exceeding $2,500 USD."

SYSTEM_PROMPT = f"""You are an elite Sales Qualifications Engine. Your sole purpose is to evaluate incoming service leads against a strict Ideal Customer Profile (ICP) and output your evaluation as a strictly formatted, valid JSON object. Do not output markdown, explanations, or any text outside of the JSON object.

THE IDEAL CUSTOMER PROFILE (ICP):
"{ICP}"

SCORING RUBRIC (0.00 to 1.00):
- 1.00: Perfect match (High budget, bespoke CMS/WordPress, CRM integration specifically requested).
- 0.80 - 0.99: Strong match (High budget, CMS/WordPress, but CRM integration implies or is negotiable).
- 0.50 - 0.79: Partial match (Needs CMS but budget is borderline, or budget is high but platform is ambiguous).
- 0.00 - 0.49: Poor match (Low budget, simple template work, no CRM needs, e-commerce only like Shopify).

JSON SCHEMA TO RETURN:
{{
  "lead_id": "string",
  "qualification_score": 0.00,
  "justification": "string (1 sentence maximum)"
}}"""

def evaluate_lead(lead_dict):
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("[Brain] Warning: NVIDIA_API_KEY missing. Mocking score execution.")
        # Very crude mock calculation based on prompt hints
        score = 0.95 if "WordPress" in lead_dict.get("title", "") and "CRM" in lead_dict.get("description", "") else 0.30
        return {
            "lead_id": lead_dict.get("lead_id"),
            "qualification_score": score,
            "justification": "Mocked logic because no API Key was supplied."
        }
        
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    user_message = f"""Evaluate the following lead based on the ICP:

Lead ID: {lead_dict.get('lead_id')}
Title: {lead_dict.get('title')}
Budget: {lead_dict.get('budget')}
Location: {lead_dict.get('location')}
Description: {lead_dict.get('description')}

Provide the strictly formatted JSON evaluation."""

    print(f"[Brain] Evaluating lead {lead_dict.get('lead_id')} via NVIDIA API...")
    
    try:
        response = client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.0, # Absolute determinism for reasoning extraction
            max_tokens=300
        )
        
        response_text = response.choices[0].message.content
        
        # Robust parsing to handle potential markdown artifacts from the LLM
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].strip()
            
        data = json.loads(response_text)
        return data
    except Exception as e:
        print(f"[Brain] Error parsing LLM JSON response: {e}")
        return {
            "lead_id": lead_dict.get("lead_id"),
            "qualification_score": 0.0,
            "justification": f"Exception encountered: {str(e)}"
        }
