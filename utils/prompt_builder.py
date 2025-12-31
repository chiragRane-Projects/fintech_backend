def build_prompt(data: dict) -> str:
    return f"""
You are generating text for a consumer fintech application.

Explain the user's financial outlook based ONLY on the data provided.

Formatting rules (MANDATORY):
- Use plain natural language
- Write 2–3 short paragraphs
- Do NOT use bullet points
- Do NOT use lists
- Do NOT use markdown
- Do NOT use asterisks (*)
- Do NOT use headings or titles
- Do NOT use emojis or symbols

Content rules:
- Do NOT give advice
- Do NOT suggest actions
- Do NOT invent or assume numbers
- Do NOT repeat raw numbers mechanically
- Summarize insights like a human financial analyst

Tone:
- Professional
- Neutral
- Calm
- Explanatory

Financial data:
{data}
"""
