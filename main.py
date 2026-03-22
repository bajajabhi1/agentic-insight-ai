import os
from typing import List, Optional
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp
from openai import OpenAI
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# --- Configuration ---
FIRECRAWL_API_KEY = "your_firecrawl_key"
OPENAI_API_KEY = "your_openai_key"
client = OpenAI(api_key=OPENAI_API_KEY)
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# --- Data Model ---
class BusinessAnalysis(BaseModel):
    name: str
    offering: str
    key_features: List[str]
    pricing_model: str = Field(description="Subscription, Free, Custom, etc.")
    source_type: str = Field(description="Open Source or Closed Source")
    target_audience: str
    demographics: str

class MarketReport(BaseModel):
    companies: List[BusinessAnalysis]

# --- Core Logic ---
class AgenticResearcher:
    def __init__(self):
        self.targets = ["base44.com", "radish.build", "paperclip.ing", "nemoclaw.ai"]
        self.results = []

    def discover_competitors(self, query: str, count: int = 20):
        """Discovers URLs using search."""
        print(f"Searching for: {query}...")
        # In a full app, use a search API here to populate self.targets
        pass

    def scrape_and_analyze(self, url: str) -> Optional[BusinessAnalysis]:
        """Scrapes a URL and uses LLM to extract structured data."""
        print(f"Analyzing {url}...")
        try:
            # 1. Scrape to Markdown
            scrape_result = app.scrape_url(url, params={"formats": ["markdown"]})
            content = scrape_result["markdown"][:10000] # Limit context

            # 2. LLM Extraction
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "Extract business details for this Agentic AI company."},
                    {"role": "user", "content": content}
                ],
                response_format=BusinessAnalysis,
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None

    def run(self):
        for url in self.targets:
            analysis = self.scrape_and_analyze(url)
            if analysis:
                self.results.append(analysis)
        
        self.generate_report()

    def generate_report(self):
        """Generates the final comparison table."""
        print("Generating Comparison Table...")
        markdown_table = "| Name | Offering | Source | Pricing | Audience |\n|---|---|---|---|---|\n"
        for c in self.results:
            markdown_table += f"| {c.name} | {c.offering} | {c.source_type} | {c.pricing_model} | {c.target_audience} |\n"
        
        with open("comparison_report.md", "w") as f:
            f.write(markdown_table)
        print("Report saved to comparison_report.md")

if __name__ == "__main__":
    researcher = AgenticResearcher()
    researcher.run()