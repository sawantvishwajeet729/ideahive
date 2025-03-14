#import libraries
import streamlit as st
import time
import os
from src import *

#setup environment and secret keys
#os.environ['OPENAI_API_KEY']=st.secrets['openai_key']
#groq_key= st.secrets['groq_key']

os.environ['OPENAI_API_KEY']="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"
groq_key="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"


# LLm model selection
model_name = {
        'Llama': 'llama-3.3-70b-versatile',
        'DeepSeek': 'deepseek-r1-distill-llama-70b',
        'Gemma': 'gemma2-9b-it',
        'Mixtral': 'mixtral-8x7b-32768'
    }

# Configure page
st.set_page_config(
    page_title="IdeaHive",
    page_icon="🐝",
    layout="wide"
)
# Custom CSS styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F3F3F3;
    }
    [data-testid="stSidebar"] {
        background-color: #f0e6ef !important;
    }
    /* Navigation links styling */
    .nav-link {
        font-size: 18px;
        color: #2d3436 !important;
        padding: 8px 0;
        cursor: pointer;
        text-decoration: none !important;
    }
    .nav-link:hover {
        color: #6c5ce7 !important;
        text-decoration: underline !important;
    }
    .active-link {
        font-weight: 600;
        color: #6d597a !important;  
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Get current page from query parameters
params = st.query_params
current_page = params.get("page", "home")

# Sidebar navigation
with st.sidebar:
    st.sidebar.image("artifacts/idea_hive.png", width=150)
    st.markdown("---")
    
    # Create navigation links with proper styling
    pages = {
        "home": "🏠 Home",
        "about": "ℹ️ About",
        "donate": "❤️ Donate"
    }
    
    for page_key, page_label in pages.items():
        is_active = "active-link" if page_key == current_page else ""
        st.markdown(
            f'<a class="nav-link {is_active}" href="?page={page_key}" target="_self">{page_label}</a>',
            unsafe_allow_html=True
        )

# Page content
if current_page == "home":
    #st.image("artifacts/idea_hive.png", width=300)
    st.markdown('<h1 class="title">💡 Idea Hive</h1>', unsafe_allow_html=True)
    st.write(
        """
        **Introducing IdeaHive 🌟**

Where Reddit's wisdom transforms into **your next big business breakthrough**.

IdeaHive taps into the pulse of real-world problems discussed by millions on Reddit. Simply enter a topic, and our AI scours threads, analyzes pain points, and delivers actionable business ideas tailored to unmet needs. Whether you're an entrepreneur, side hustler, or innovator, IdeaHive turns Reddit's candid conversations into your roadmap for success.
"""
    )

    st.write("---")

    #clear any previous
    st.session_state.clear()

    #column sections for selecting llm model and entering the area of interest
    columns = st.columns(2, gap='large', vertical_alignment="center")

    #for llm selection
    with columns[0]: 
        option = st.selectbox(
        "Select your LLM model",
        ( "Llama",
            "DeepSeek", 
            "Gemma",
            "Mixtral"
        ))

        # Add custom CSS for selectbox styling
        st.markdown("""
        <style>
        /* Style selectbox */
        div[data-testid="stSelectbox"] {
            width: 200px;
        }
        
        div[data-testid="stSelectbox"] > div > div {
            border: 2px solid #e56b6f;
            border-radius: 8px;
        }
        
        /* Style selectbox on hover */
        div[data-testid="stSelectbox"] > div > div:hover {
            border-color: #355070;
        }

        /* Style chat input textbox */
        .stChatInput {
            border: 2px solid #e56b6f !important;
            border-radius: 8px !important;
        }
        
        .stChatInput:hover, .stChatInput:focus {
            border-color: #355070 !important;
        }
        </style>
    """, unsafe_allow_html=True)
        
    #selected llm model
    llm_model = model_name[option]

    #for entering the area of interet
    with columns[1]:
        st.write("")
        st.session_state['subject'] = st.chat_input("Type the Area of Interest")
    
    #deepk has reasoning cpabilities. Hence giving out a warning
    if llm_model=='deepseek-r1-distill-llama-70b':
        st.warning('This is a reasoning model', icon="⚠️")

    #get the post related to the area of interest from reddit
    combined_post, num_post = get_post(subject=st.session_state['subject'], limit=20)

    #only run the vector embedding and llm if there are posts related to the subject selected
    if num_post>0:
        if st.session_state['subject']:
            with st.spinner("Analyzing Reddit posts and generating business ideas..."):
                vector_retriever = vector_embeddings(combined_post)
                post_summary = post_cot(vector_retriever, st.session_state['subject'],  groq_key=groq_key,)
                idea_output = get_idea(post_summary, groq_key=groq_key, model = llm_model, subject=st.session_state['subject'])

                #stream the output
                def stream_data():
                    for word in idea_output.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                with st.container():
                    st.subheader(f"Here's a business idea related to {st.session_state['subject']}")
                    st.write_stream(stream_data)
    else:
        with st.container():
            st.write("Sorry 🙁, there are no posts on Reddit related to this topic")


elif current_page == "about":
    # About Section
    st.markdown('<div id="about"></div>', unsafe_allow_html=True)
    st.header("📜 About Idea Hive")
    st.write(
        """
        **Idea Hive**- Where Reddit's wisdom transforms into your next **big business breakthrough**.  
        - **How It Works:**  
        1. Extracts reddit posts realted to the topic. Currently the number of posts is limited to 20. Since vector embedding costs 💰
        2. Converts text into vectors using OpenAI embeddings and FAISS  
        3. Generates business ideas using multiple large language models  

        Whether you're an entrepreneur, side hustler, or innovator, IdeaHive turns Reddit's candid conversations into your roadmap for success! 🚀
        """
    )
    
    with st.container():
        st.header('✉️ Connect with me')
        st.write("[Email >](sawantvishwajeet729@gmail.com)")
        st.write("[LinkedIn >](https://www.linkedin.com/in/sawantvishwajeet729/)")
        st.write("[Medium >](https://medium.com/@sawantvishwajeet729)")
        st.write("[Github >](https://github.com/sawantvishwajeet729)")

elif current_page == "donate":
    #donate section
    st.markdown('<div id="Donate"></div>', unsafe_allow_html=True)
    st.header("☕ Donate")
    st.write (
        """
        Hey there! 😊 Love Idea Miner ? 🚀 Support me to keep it running and making new free web apps! Every little bit helps. 💙 Thank you!
        
        """
    )
    st.write("")
    st.markdown(
    """
    <style>
    .donate-button {
        background-color: #ef476f;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
        transition: transform 0.2s ease-in-out;
    }
    .donate-button:hover {
        transform: scale(1.05);
        color:white;
        background-color: #C8385A;
    }
    </style>
    
    <a class="donate-button" href="https://github.com/sponsors/sawantvishwajeet729" target="_blank">
        Buy me a Coffee 🧋
    </a>
    """,
    unsafe_allow_html=True
)
# Footer
st.divider()
columns_footer = st.columns(4)
with columns_footer[0]:
    st.caption("2025 IdeaHive.")

with columns_footer[3]:
    st.caption("Made with ❤️ by Vishwajeet Sawant", help=None, unsafe_allow_html=True)

