import anthropic, os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def read_10k(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_section(text, prompt):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": f"{prompt}\n\n{text}"}]
    )
    return message.content[0].text

if __name__ == "__main__":
    text = read_10k("duolingo_10k.txt")

    risks = analyze_section(
        text[:50000],
        "Give me most threatening risks to Duolingo, risks that are actually possible at happening."
    )

    mda = analyze_section(
        text[50000:100000],
        "Summarize how Duolingo is performing."
    )

    print("=== KEY RISKS ===\n", risks)
    print("\n=== MD&A SUMMARY ===\n", mda)