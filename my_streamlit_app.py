import streamlit as st
from news_api123 import NewsAPI  # Adjusted import statement
from news_video import VideoGenerator  # Adjusted import statement
from dotenv import load_dotenv
import os
load_dotenv()
news_api_key = "enter the newsapi key"
news_client = NewsAPI(news_api_key=news_api_key)  
did_api_key = "enter the did apikey"
username, password = did_api_key.split(':')
video_gen = VideoGenerator(username, password)  # Corrected instance name
st.set_page_config(
    page_title="AI News Anchor",
    layout="wide"
)
st.title("AI News Anchor")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('Built with Midjourney, OpenAI, D-ID, Streamlit and ❤️')
st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)
image_url = st.text_input("Enter Image URL", "https://i.ibb.co/fHMz4gb/A-beautiful-news-caster-standing-in-front-of-the-c.jpg")
query = st.text_input("Enter Query Keywords", "query")
num_news = st.slider("Number of News", min_value=1, max_value=5, value=3)
if st.button("Generate"):
    if image_url.strip() and query.strip() and num_news is not None and num_news > 0:
        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            st.info("Your AI News Anchor: Sophie")
            st.image(image_url, caption="Anchor Image", use_column_width=True)

        with col2:
            desc_list = news_client.get_news_descriptions(query, num_news=num_news)
            st.success("Your Fetched News")
            st.write(desc_list)
            
            #to get a concatenated string of descriptions
            # desc_string = news_client.get_news_string(query, num_news=num_news)
            numbered_paragraphs = "\n".join([f"{i+1}. {paragraph}" for i, paragraph in enumerate(desc_list)])
            st.write(numbered_paragraphs)


        with col3:
            final_text = f"""
                Hello World, I'm Sophie, your AI News Anchor. Bringing you the latest updates for {query}.
                Here are the news for you: {numbered_paragraphs}
                That's all for today. Stay tuned for more news, Thank you!
            """

            video_url = video_gen.generate_video(final_text, image_url)

            st.warning("AI News Anchor Video")
            st.video(video_url)
    
    else:
        st.write("Failed to fetch news data. Please check your query and API key.")
