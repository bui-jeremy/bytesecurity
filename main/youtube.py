from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings

# Define the API key.
YOUTUBE_API_KEY = 'AIzaSyDf8Q86hjf2qTWeadFo_zle2aA7nc0heJs'

# Define the YouTube API client.
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def search_videos(query):
    """
    Search for YouTube videos based on a given query string.

    Args:
        query (str): The search query string.

    Returns:
        A list of dictionaries containing information about each video,
        including the video ID, title, description, and thumbnail URL.
    """
    try:
        # Call the YouTube API to search for videos.
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=5,
            order='relevance'
        ).execute()

        videos = []
        for item in search_response['items']:
            video = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail_url': item['snippet']['thumbnails']['default']['url']
            }
            videos.append(video)

        return videos

    except HttpError as e:
        print('An error occurred: %s' % e)
        return []