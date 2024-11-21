import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

from codes.story_extract import getstory
from scipy import stats

def filter_anomalies(df, threshold=3):
    """Filters out extreme anomalies based on Z-score."""
    # Calculate the Z-scores of sentiment values
    z_scores = stats.zscore(df['Sentiment'])
    
    # Create a mask to filter out anomalies (Z-scores above the threshold)
    mask = (z_scores > -threshold) & (z_scores < threshold)
    
    # Filter the DataFrame to exclude anomalies
    filtered_df = df[mask]
    
    return filtered_df


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

    Subreddit_link = st.text_input("Enter subreddit URL: ")

    if st.button("Fetch and Analyze Comments"):
        if not Subreddit_link:
            Subreddit_link = LINK
        
        with st.spinner("Fetching Posts..."):
            comments_data = getstory(Subreddit_link)

        st.success(f"Total interactions fetched: {len(comments_data)}")

        df = pd.DataFrame(comments_data, columns=["Subreddit", "Title", "Selftext", "Author", "Upvote Ratio", "Sentiment", "Time"])

        # Apply anomaly filter before further analysis
        filtered_df = filter_anomalies(df)
        st.write(f"Filtered out {len(df) - len(filtered_df)} anomalies")

        st.dataframe(filtered_df)

        st.subheader("Sentiment Distribution (Filtered)")
        fig, ax = plt.subplots()
        filtered_df['Sentiment'].plot(kind='hist', bins=20, ax=ax, title="Sentiment Distribution of Comments (Filtered)")
        st.pyplot(fig)

        st.subheader("Sentiment Over Time (Filtered)")
        filtered_df['Time'] = pd.to_datetime(filtered_df['Time'])
        filtered_df = filtered_df.sort_values(by='Time')
        fig, ax = plt.subplots()
        ax.plot(filtered_df['Time'], filtered_df['Sentiment'], marker='o', linestyle='-', color='b')
        ax.set_xlabel('Time')
        ax.set_ylabel('Sentiment')
        ax.set_title('Sentiment Over Time (Filtered)')
        st.pyplot(fig)

        avg_sentiment = filtered_df['Sentiment'].mean()
        score = calculate_score(avg_sentiment)
        st.subheader(f"Overall Sentiment Score (Filtered): {score:.2f}/100")

        fig = draw_gauge_chart(score)
        st.pyplot(fig)

        threshold = 0.1
        if avg_sentiment >= threshold:
            st.success("Based on the current analysis, the emotions are positive.")
        else:
            st.warning("Based on the current analysis, the emotions are negative.")

        csv = filtered_df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name='filtered_comments_with_sentiment.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
    