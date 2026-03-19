import os
import json
import random
import time
from playwright.sync_api import sync_playwright

def scrape_bark_leads(mock_mode=True):
    print("[Scraper] Initializing data acquisition module...")
    if mock_mode:
        return _mock_scrape()
    return _real_scrape()

def _mock_scrape():
    """Mock fallback for PoC purposes to avoid requiring actual Bark.com accounts."""
    time.sleep(1.5)
    return [
        {
            "lead_id": "L-1001",
            "title": "Bespoke Headless WordPress integration",
            "budget": "$5,500+",
            "location": "Remote, US",
            "description": "We require a senior developer to build a headless WordPress site using Next.js. Must integrate with Salesforce CRM. High performance is critical."
        },
        {
            "lead_id": "L-1002",
            "title": "Simple Shopify Store Setup",
            "budget": "$500",
            "location": "London, UK",
            "description": "Need a basic e-commerce store setup using a standard Shopify theme. No custom features or integrations required."
        }
    ]

def _real_scrape():
    """Real Playwright scraping execution. Requires valid DOM layout and credentials."""
    email = os.getenv("BARK_EMAIL")
    password = os.getenv("BARK_PASSWORD")
    
    leads = []
    with sync_playwright() as p:
        # Launch browser with human-like viewport
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            record_video_dir="/Users/manharnakhuva/.gemini/antigravity/brain/5a1da5c4-b27a-425f-b9e8-ecc52c6adfe4/",
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        print("[Scraper] Navigating to Bark.com...")
        page.goto("https://www.bark.com/en/us/sellers/dashboard/")
        
        # Simulated Authentication
        if page.locator('input[name="email"]').is_visible():
            print("[Scraper] Logging in...")
            page.type('input[name="email"]', email, delay=random.randint(50, 150))
            page.type('input[name="password"]', password, delay=random.randint(50, 150))
            page.click('button[type="submit"]')
            # Wait for any API calls to complete reliably
            page.wait_for_load_state("networkidle")
            
        print("[Scraper] Extracting leads from Buyer Requests...")
        try:
            page.wait_for_timeout(3000)
            print("[Scraper] Taking screenshot of the dashboard...")
            page.screenshot(path="/Users/manharnakhuva/.gemini/antigravity/brain/5a1da5c4-b27a-425f-b9e8-ecc52c6adfe4/dashboard_screenshot.png")
            
            page.wait_for_selector('.lead-card-container', timeout=5000)
            lead_cards = page.locator('.lead-card-container').all()
            
            for i, card in enumerate(lead_cards):
                # Robust extraction utilizing is_visible checks
                title = card.locator('.lead-title').inner_text() if card.locator('.lead-title').is_visible() else "N/A"
                description = card.locator('.lead-description-text').inner_text() if card.locator('.lead-description-text').is_visible() else "N/A"
                budget = card.locator('[data-test-id="lead-budget"]').inner_text() if card.locator('[data-test-id="lead-budget"]').is_visible() else "N/A"
                location = card.locator('.location-badge').inner_text() if card.locator('.location-badge').is_visible() else "N/A"
                
                leads.append({
                    "lead_id": f"LIVE-{i}",
                    "title": title,
                    "budget": budget,
                    "location": location,
                    "description": description
                })
        except Exception as e:
            print(f"[Scraper] Warning: Could not scrape live DOM: {e}")
            
        context.close()
        browser.close()
    return leads
