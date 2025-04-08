from config import GEMINI_API_KEY
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

def analyze_titles_with_gemini(titles):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "I have a list of YouTube video titles. Choose the one that is the most relevant, useful, and engaging.\n"
        "Consider clarity, appeal, and how well the title fits the likely viewer intent.\n"
        "Here are the titles:\n\n"
    )
    for i, title in enumerate(titles, 1):
        prompt += f"{i}. {title}\n"
    
    prompt += "\nPlease reply with:\n- The best title\n- Its index\n- A short reason why you selected it."
    response = model.generate_content(prompt)
    return response.text
