from config import YOUTUBE_API_KEY
import requests
import datetime
from utils import convert_duration_to_minutes

SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
VIDEO_DETAILS_URL = 'https://www.googleapis.com/youtube/v3/videos'

def search_youtube(query, max_results=50):
    today = datetime.datetime.now()
    fourteen_days_ago = today - datetime.timedelta(days=14)

    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'publishedAfter': fourteen_days_ago.isoformat("T") + "Z",
        'maxResults': max_results,
        'key': YOUTUBE_API_KEY
    }

    response = requests.get(SEARCH_URL, params=params)
    results = response.json()
    video_ids = [item['id']['videoId'] for item in results.get('items', [])]
    return video_ids

def get_video_details(video_ids, sort_by="views"):
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': ','.join(video_ids),
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(VIDEO_DETAILS_URL, params=params)
    video_data = response.json()

    videos = []
    for item in video_data.get('items', []):
        duration = convert_duration_to_minutes(item['contentDetails']['duration'])
        if not (4 <= duration <= 20):
            continue

        video = {
            'title': item['snippet']['title'],
            'video_id': item['id'],
            'duration_mins': round(duration, 2),
            'published_at': item['snippet']['publishedAt'],
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0)) if 'likeCount' in item['statistics'] else 0
        }
        videos.append(video)

    if sort_by == "views":
        videos.sort(key=lambda x: x['views'], reverse=True)
    elif sort_by == "likes":
        videos.sort(key=lambda x: x['likes'], reverse=True)
    elif sort_by == "newest":
        videos.sort(key=lambda x: x['published_at'], reverse=True)
    elif sort_by == "oldest":
        videos.sort(key=lambda x: x['published_at'])

    return videos[:20]
