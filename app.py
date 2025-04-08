import streamlit as st
from youtube_api import search_youtube, get_video_details
from gemini_analysis import analyze_titles_with_gemini

st.title("🎥 YouTube Video Analyzer")
query = st.text_input("Enter a video topic (e.g., 'AI tools for students'):")
sort_by = st.selectbox("Sort results by:", ["views", "likes", "newest", "oldest"])

if st.button("Search"):
    if not query:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Fetching YouTube data..."):
            video_ids = search_youtube(query)
            filtered_videos = get_video_details(video_ids, sort_by)

        st.subheader("📋 Top Videos")
        for i, video in enumerate(filtered_videos, 1):
            st.markdown(f"**{i}. {video['title']}**")
            st.markdown(f"- ⏱ Duration: {video['duration_mins']} mins")
            st.markdown(f"- 👁 Views: {video['views']}")
            st.markdown(f"- 👍 Likes: {video['likes']}")
            st.markdown(f"- 📅 Published: {video['published_at']}")
            st.markdown(f"- 🔗 [Watch Video](https://www.youtube.com/watch?v={video['video_id']})")
            st.markdown("---")

        if st.button("🔍 Analyze with Gemini"):
            titles = [v['title'] for v in filtered_videos]
            with st.spinner("Analyzing titles..."):
                gemini_response = analyze_titles_with_gemini(titles)
            st.subheader("Gemini's Analysis")
            st.markdown(gemini_response)
