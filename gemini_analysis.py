from config import GEMINI_API_KEY
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

def analyze_titles_with_gemini(videos):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "You're a smart video assistant. I have a list of YouTube videos with metadata.\n"
        "Recommend the best one to watch.\n"
        "Pick the most interesting, valuable, or entertaining video based on:\n"
        "- Views\n"
        "- Likes\n"
        "- Duration\n"
        "- Title appeal\n"
        "\nGive a friendly recommendation and explain why you picked it.\n"
        "You can highlight if the video is viral, funny, trending, educational, etc.\n"
        "Mention the views, likes, and anything interesting in your reasoning.\n\n"
        "Here are the videos:\n\n"
    )
    for idx, video in enumerate(videos, 1):
        prompt += (
            f"{idx}. Title: {video['title']}\n"
            f"   Duration: {round(video['duration_mins'], 2)} mins\n"
            f"   Views: {video['views']}\n"
            f"   Likes: {video['likes']}\n"
            f"   Published At: {video['published_at']}\n"
            f"   Link: https://www.youtube.com/watch?v={video['video_id']}\n\n"
        )

    prompt += (
        "Now, reply with:\n"
        "- The title and index of the best video to watch\n"
        "- A short, clear reason why it's recommended\n"
        "- Mention any stats that support your recommendation\n"
        "- Sound like you're suggesting it to a friend"
    )

    response = model.generate_content(prompt)
    return response.text