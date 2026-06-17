import anthropic, os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_section(text, prompt):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": f"{prompt}\n\n{text}"}]
    )
    return message.content[0].text

def chunk_text(text, max_chars=6000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def extract_qa(transcript):
    qa_start = transcript.find("Question-and-Answer Session")
    if qa_start == -1:
        qa_start = transcript.find("QUESTION AND ANSWER")
    if qa_start == -1:
        qa_start = transcript.find("Q&A")
    return transcript[qa_start:] if qa_start != -1 else transcript

def summarize_earnings(transcript):
    qa_section = extract_qa(transcript)
    
    prompt = """Analyze this earnings call transcript and provide:
1. Management's top 3 talking points (what they emphasized most)
2. Analyst pushback (what analysts pushed back on or were skeptical about)
3. Any guidance changes (did they raise, lower, or maintain guidance?)

Be concise and specific."""
    
    return analyze_section(qa_section[:10000], prompt)

if __name__ == "__main__":
    with open("company1_earnings.txt", "r", encoding="utf-8") as f:
        transcript = f.read()
    
    result = summarize_earnings(transcript)
    print(result)