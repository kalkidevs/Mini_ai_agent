import os
from openai import OpenAI

SYSTEM_PROMPT = """You are an expert technical sales executive. Your goal is to draft a highly personalized, persuasive proposal response to a qualified lead.

CONSTRAINTS & RULES:
1. The response MUST be exactly three paragraphs long.
2. Paragraph 1: An engaging hook establishing relevance.
3. Paragraph 2: Our specific technical approach to their problem.
4. Paragraph 3: A soft call-to-action (CTA) to schedule a brief discovery call.
5. NON-NEGOTIABLE CORE REQUIREMENT: You MUST identify and seamlessly integrate at least TWO distinct, verifiable data points directly extracted from their Lead Description (e.g., quoting a specific feature they asked for, referencing their current tech stack, or acknowledging their timeline/budget constraints). Use these data points organically to prove we read their brief.

Do not include a Subject Line. Do not include placeholder text like "[Your Name]". Just output the three-paragraph body text cleanly."""

def generate_proposal(lead_dict, justification):
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("[Communicator] Warning: NVIDIA_API_KEY missing. Mocking generated response.")
        return f"Mock Paragraph 1: Great to see you're looking for '{lead_dict.get('title')}'.\n\nMock Paragraph 2: Based on your budget of {lead_dict.get('budget')} we can perfectly help with your {lead_dict.get('location')} based setup.\n\nMock Paragraph 3: Let's schedule a call."
        
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    user_message = f"""Draft a proposal for this exact requested project:

Title: {lead_dict.get('title')}
Budget: {lead_dict.get('budget')}
Description: {lead_dict.get('description')}
AI Brain Justification for Qualification: {justification}"""

    print(f"[Communicator] Drafting highly contextual proposal for {lead_dict.get('lead_id')} via NVIDIA API...")
    
    try:
        response = client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7, # Slight creativity requested for compelling copy
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[Communicator] Error generating proposal: {e}")
        return "Error occurred during LLM text generation."
