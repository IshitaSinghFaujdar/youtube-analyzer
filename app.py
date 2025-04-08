import streamlit as st
from youtube_api import search_youtube, get_video_details
from gemini_analysis import analyze_titles_with_gemini

st.title("🎥 YouTube Video Title Analyzer")

# Input for video search query
query = st.text_input("Enter a video topic (e.g., 'AI tools for students'):")

# Sorting options
sort_by = st.selectbox("Sort by:", ["views", "likes", "duration", "newest", "oldest"])
ascending = st.checkbox("Sort in ascending order?", value=False)

if st.button("🔍 Analyze with Gemini"):
    if not query:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Fetching YouTube data..."):
            video_ids = search_youtube(query)
            filtered_videos = get_video_details(video_ids, sort_by, ascending)

        if not filtered_videos:
            st.error("No suitable videos found.")
        else:
            titles = [v['title'] for v in filtered_videos]

            with st.spinner("Analyzing video titles using Gemini..."):
                gemini_response = analyze_titles_with_gemini(filtered_videos)

            st.subheader("📊 Gemini's Analysis")
            st.markdown(gemini_response)
