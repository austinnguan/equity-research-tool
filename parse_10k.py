import anthropic, os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def read_10k(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_section(text, start_item, end_item):
    # Every 10-K lists its items twice: once in the table of contents,
    # once for real. Starting the search at 10,000 skips the TOC.
    start = text.index(f"\n{start_item}", 10000)
    end   = text.index(f"\n{end_item}", start)
    return text[start:end]

def analyze_section(text, prompt):
    message = client.messages.create(
        model="claude-opus-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": f"{prompt}\n\n{text}"}]
    )
    # Opus 5 can return a thinking block first, so find the text block
    # instead of assuming it's content[0].
    for block in message.content:
        if block.type == "text":
            return block.text
    return ""

if __name__ == "__main__":
    text = read_10k("chipotle_10k.txt")

    risks = analyze_section(
        get_section(text, "ITEM 1A.", "ITEM 2."),
        "Give me the most threatening risks to Chipotle, risks that are actually plausible."
    )

    mda = analyze_section(
        get_section(text, "ITEM 7.", "ITEM 8."),
        "Summarize how Chipotle is performing."
    )

    print("=== KEY RISKS ===\n", risks)
    print("\n=== MD&A SUMMARY ===\n", mda)