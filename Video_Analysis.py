import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

def extract_video_id(url):
    video_id_match = re.search(r'(?<=v=)[^&]+', url)
    if video_id_match:
        return video_id_match.group(0)
    else:
        return None

def get_yt_client(api_key):
    return build("youtube", "v3", developerKey=api_key)

def get_comments(client, video_id, token=None):
    try:
        response = client.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,
            pageToken=token,
        ).execute()
        return response
    except HttpError as e:
        st.error(f"HTTP Error: {e.resp.status}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def calculate_score(sentiment):
    score = (sentiment + 1) * 50
    return score

def draw_gauge_chart(score):
    fig, ax = plt.subplots()

    
    circle = plt.Circle((0.5, 0.5), 0.4, color='white', fill=True)
    ax.add_artist(circle)

    
    wedge = Wedge((0.5, 0.5), 0.4, 0, score * 3.6, facecolor='green', edgecolor='gray', linewidth=2)
    ax.add_patch(wedge)

    
    bg_wedge = Wedge((0.5, 0.5), 0.4, score * 3.6, 360, facecolor='lightgray', edgecolor='gray', linewidth=2)
    ax.add_patch(bg_wedge)

    
    plt.text(0.5, 0.5, f'{score:.1f}%', horizontalalignment='center', verticalalignment='center', fontsize=20, color='black')

    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    plt.axis('off')

    return fig

def main():
    st.title("YouTube Comments Sentiment Analysis")

    api_key = "AIzaSyAUt9ULu5G7EO4WUkSsNcjeaamHSWBDmX4"

    video_url = st.text_input("Enter YouTube Video URL: ")

    if st.button("Fetch and Analyze Comments"):
        if not api_key:
            st.error("Please enter a valid YouTube API key.")
            return

        if not video_url:
            st.error("Please enter a valid YouTube video URL.")
            return

        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL")
            return

        yt_client = get_yt_client(api_key)

        comments = []
        next_page_token = None

        with st.spinner("Fetching comments..."):
            while True:
                resp = get_comments(yt_client, video_id, next_page_token)

                if not resp:
                    break

                comments.extend(resp["items"])
                next_page_token = resp.get("nextPageToken")
                if not next_page_token:
                    break

        st.success(f"Total comments fetched: {len(comments)}")

        comments_data = [
            {
                "Author": comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                "Comment": comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                "Likes": comment["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                "Time": comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                "Sentiment": analyze_sentiment(comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            }
            for comment in comments
        ]

        df = pd.DataFrame(comments_data, columns=["Author", "Comment", "Likes", "Time", "Sentiment"])

        st.dataframe(df)

        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        df['Sentiment'].plot(kind='hist', bins=20, ax=ax, title="Sentiment Distribution of Comments")
        st.pyplot(fig)

        st.subheader("Sentiment Over Time")
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.sort_values(by='Time')
        fig, ax = plt.subplots()
        ax.plot(df['Time'], df['Sentiment'], marker='o', linestyle='-', color='b')
        ax.set_xlabel('Time')
        ax.set_ylabel('Sentiment')
        ax.set_title('Sentiment Over Time')
        st.pyplot(fig)

        avg_sentiment = df['Sentiment'].mean()
        score = calculate_score(avg_sentiment)
        st.subheader(f"Overall Sentiment Score: {score:.2f}/100")

        fig = draw_gauge_chart(score)
        st.pyplot(fig)

        threshold = 0.1
        if avg_sentiment >= threshold:
            st.success("Based on the comments analysis, this video is considered useful.")
        else:
            st.warning("Based on the comments analysis, this video is not considered useful.")

        csv = df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='comments_with_sentiment.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
    