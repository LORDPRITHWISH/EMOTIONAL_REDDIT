import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

from codes.story_extract import getstory


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

def main(LINK):
    st.title("Reddit Comments Sentiment Analysis")

    # api_key = "AIzaSyAUt9ULu5G7EO4WUkSsNcjeaamHSWBDmX4"

    Subreddit_link = st.text_input("Enter subreddit URL: ")
    

    if st.button("Fetch and Analyze Comments"):
        # if not api_key:
        if not Subreddit_link:
            Subreddit_link = LINK
        

        with st.spinner("Fetching Posts..."):
            while True:
                comments_data = getstory(Subreddit_link)
                break

        st.success(f"Total interacations fetched: {len(comments_data)}")

        df = pd.DataFrame(comments_data, columns=["Subreddit", "Title", "Selftext","Author", "Upvote Ratio", "Sentiment", "Time"])

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
            st.success("Based on the current analysis, the emotions are positive.")
        else:
            st.warning("Based on the current analysis, the emotions are negative.")

        csv = df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='comments_with_sentiment.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
    