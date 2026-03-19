# 🤖 Bark AI Autonomous Agent - Proof of Concept

<div align="center">
  <h3>Intelligent Lead Scraping, AI Qualification, & Automated Pipeline</h3>
  <p>A Python-powered AI Agent engineered to autonomously browse Bark.com, extract service leads, evaluate semantic fit using NVIDIA's Llama 3.1 70B, and formulate highly-personalized sales pitches.</p>
</div>

---

## 🚀 Key Features

- 🕵️ **Autonomous Web Navigation:** Uses **Playwright** to navigate portals and simulate human interactions, efficiently waiting for dynamically-loaded DOM elements.
- 🧠 **Intelligent Qualification:** Configured with the **NVIDIA NIM API** (utilizing the `openai` Python SDK) to rapidly score raw lead descriptions against an Ideal Customer Profile (ICP).
- ✍️ **Contextual Communicator:** Bypasses boilerplate pitches by explicitly forcing the LLM to organically embed at least *two distinct verifiable data points* directly extracted from the buyer's specific request. 

---

## 🛠️ Tech Stack 

- **Python** - Core logic architecture.
- **Playwright** - Robust Chromium automation supporting DOM timeouts and structural scraping.
- **NVIDIA Build (Llama 3.1 70B)** - Lightning-fast inference driving the semantic evaluation.

---

## 📖 Quick Start Guide

Want to run the backend Agent seamlessly on your own machine? It's incredibly straightforward!

### 1️⃣ Get Your Free NVIDIA API Key
1. Go to **[NVIDIA AI Platform](https://build.nvidia.com/explore/discover)**.
2. Sign in and select a model (e.g., `Llama 3.1 70B Instruct`).
3. Generate and copy your API Key (`nvapi-...`).

### 2️⃣ Configure Local Credentials
Rename the `.env.example` file to `.env` and paste your key along with your Bark credentials:

```text
BARK_EMAIL=your_email@example.com
BARK_PASSWORD=your_password
NVIDIA_API_KEY=your_nvidia_api_key
```

### 3️⃣ Installation
Open your terminal, create an isolated virtual environment, and install the required dependencies:
```bash
# 1. Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate  # (Use `venv\Scripts\activate` if on Windows)

# 2. Install Packages
pip install -r requirements.txt
playwright install chromium
```

### 4️⃣ Execution
Trigger the complete agent pipeline:
```bash
python main.py
```
> **🌟 Pro-Tip:** By default, the application runs natively in *Mock Mode* to instantly demonstrate logic flow. Open `main.py` and change the parameter to `mock_mode=False` to trigger the complete, live Chromium automation that actually browses the web!

---

## 🎬 Live Walkthrough & Demo

This system natively leverages Playwright's browser automation capability to autonomously log into your dashboard, await asynchronous content hydration, and extract lead data directly from the DOM!

### Dashboard Extraction Screenshot
Here is a snapshot of the Chromium browser safely navigating past the authentication portal into the Bark Dashboard:

![Dashboard Screenshot](./assets/dashboard_screenshot.png)

### Auto-Generated Proposal Demonstration
Based on the Lead input, the NVIDIA Llama 3.1 70B model analyzes the buyer intent and evaluates if the budget constraints match the ICP. If the score exceeds `0.8`, the Agent organically leverages distinct data points from the description to draft a three-paragraph hyper-contextual cover letter into the `outbox/` directory:

```text
[Communicator] Drafting highly contextual proposal for L-1001 via NVIDIA API...
✅ Contextual proposal safely drafted to outbox/L-1001_proposal.txt

--- Generated Cover Letter ---
Hi there! I noticed your buyer request on Bark detailing your need for a bespoke headless WordPress solution, and I was immediately drawn to the project. Your requirement for seamless integration with a custom HubSpot CRM aligns perfectly with our agency's core expertise.

Our engineers specialize in high-performance headless architecture utilizing Next.js as the front-end layer for WordPress. By decoupling the CMS, we can guarantee lightning-fast load times for your boutique agency's client. Additionally, we have extensive experience mapping complex data structures straight into HubSpot via their API, ensuring your marketing automation workflows remain uninterrupted and highly tailored to your new site.

Given your stated budget of $5,500+, we have more than enough scope to architect a premium, scalable solution that exceeds your client's expectations without compromising on speed or security. I'd love to schedule a brief discovery call this week to walk you through similar headless CRM integrations we've successfully deployed. Let me know what day works best!
------------------------------
```

### 📹 Full Execution Video
You can watch the fully automated headless-browser extraction and LLM pipeline [right here in our demo video](./assets/demo_video.webm)!

---

<div align="center">
  <i>Developed as an architectural Proof-of-Concept for autonomous Sales Qualification.</i>
</div>
