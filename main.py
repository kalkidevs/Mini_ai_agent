import os
from dotenv import load_dotenv

from scraper import scrape_bark_leads
from brain import evaluate_lead
from communicator import generate_proposal

def main(mock_mode=True):
    load_dotenv()
    
    print("=" * 60)
    print(" Bark AI Autonomous Agent - Proof of Concept Workflow")
    print("=" * 60)
    
    # 1. Scrape Leads
    leads = scrape_bark_leads(mock_mode=mock_mode)
    
    print(f"\n[Orchestrator] Discovered {len(leads)} leads. Proceeding to AI Qualification...")
    
    for lead in leads:
        print("-" * 60)
        print(f"Lead ID: {lead.get('lead_id')} | Title: {lead.get('title')}")
        
        # 2. Score Lead
        evaluation = evaluate_lead(lead)
        score = evaluation.get("qualification_score", 0.0)
        just_text = evaluation.get("justification", "")
        
        print(f"Score: {score:.2f} | Justification: {just_text}")
        
        # 3. Contextual Drafting Check
        if score > 0.8:
            print(">>> Lead Highly Qualified! Activating Communicator Module...")
            proposal = generate_proposal(lead, just_text)
            
            # 4. Outbox / Review System
            outbox_dir = "outbox"
            os.makedirs(outbox_dir, exist_ok=True)
            out_file = os.path.join(outbox_dir, f"{lead.get('lead_id')}_proposal.txt")
            
            with open(out_file, "w") as f:
                f.write(proposal)
                
            print(f"✅ Contextual proposal safely drafted to {out_file}\n")
            print("--- Generated Cover Letter ---")
            print(proposal)
            print("------------------------------")
        else:
            print(">>> Lead strictly unqualified (< 0.8). Discarding permanently.")

if __name__ == "__main__":
    # Core orchestration loop
    # Set mock_mode=False if you possess actual Bark.com auth and wish to test the stealth Playwright scraper over DOM elements.
    main(mock_mode=False)
