# equity-research-tool
This is an AI - assisted equity research workflow that helps me analyze public companies with the help of Python and Claude's API. I advise that you use this tool solely as a supplemental source to compare with your own findings.

## About
Built by Austin Guan, a NYU student studying Economics. This is one part of a summer project that combines equity research, financial modeling, and published pitches onto Substack

## What It Does
- earnings_summary.py sends a company's earnings or 10-K to Claude and returns a summary of key themes, management tone, and potential pushback. 
- parse_10k.py extracts and parses data from a 10-K that can be used for financial modeling (PDF ONLY)

## Setup
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv312`
3. Activate it: `source venv312/bin/activate`
4. Install dependencies: `pip install anthropic python-dotenv`
5. Create a `.env` file in the root directory and add your API key: ANTHROPIC_API_KEY=[your_key_here]

## Research Published
Equity pitches published at: [My Substack] (https://substack.com/@austinguan) 

## Stack
- Python 3.12
- Claude API (claude-sonnet-4-6)