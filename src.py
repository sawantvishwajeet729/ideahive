import streamlit as st
import praw
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq  
from langchain.chains import create_retrieval_chain 


def get_post(subject, time_filter="year", limit=20):
    """This function get the reddit posts related to the subject mentioned in the arguments"""

    #setup the reddit API
    reddit = praw.Reddit(
    client_id=st.secrets['client_id'],
    client_secret=st.secrets['client_secret'],
    user_agent=st.secrets['user_agent']
    )
    # Define search parameters
    time_filter = time_filter
    query = f'{subject} and (problem OR issue OR help OR advice OR "bad experience")'
    subreddit = reddit.subreddit('all')

    # Search posts sorted by comment activity
    posts = subreddit.search(query, sort='relevance', limit=limit, time_filter=time_filter)

    #create a list for strings in the posts
    post_list = []

    #loop the posts and create a string for each post
    for post in posts:
        reddit_post = f"The title of the post is: {post.title}. The number of comments on this post are: {post.num_comments}. The upvotes on this post are: {post.score}. The post is as follow: {post.selftext}"
        post_list.append(reddit_post)

    #number of posts available
    num_posts = len(post_list)

    #combine all strings in post_list into a single string
    combined_posts = " ".join(post_list)

    return combined_posts, num_posts



def vector_embeddings(all_text):
    """This function converts the text into vector embeddings"""
    #Text spliiter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300
    )
    chunks = text_splitter.split_text(all_text)

    # Create vector store from text chunks
    db = FAISS.from_texts(chunks, OpenAIEmbeddings(model="text-embedding-3-large", dimensions=1536))

    # Vector retriever from vector store
    vector_retriever = db.as_retriever()

    return vector_retriever
    

def get_idea(vector_retriever,groq_key, subject,  model = "llama-3.3-70b-versatile"):
    """This function passes the vector embeddings along with the systme prompt to the llm to analyse and get the business idea"""

    #define the prompt
    business_prompt = PromptTemplate(
    input_variables=["context", "subject"],
    template="""
    User has provided Reddit posts related to {subject}. Each post has:
    - **Post Content:** {context}
    - **Upvotes & Comments:** Higher scores mean greater importance.

    ### **Your Task:**
    Analyze these posts and generate a structured business idea following the system prompt. 
    Analyze all the post and generate a business idea that can be a solution to one or more of the problems mentioned in the posts.
    Do not fixate on single post, but rather look at the overall context and generate a business idea that can be a solution to one or more of the problems mentioned in the posts.

    **Output Format:**
    💡 **Business Idea:** (Catchy name + one-liner pitch)  
    🔍 **Problem Identified:** (What issue does this address?)  
    🚀 **Solution:** (How does this business work?)  
    🎯 **Target Market:** (Who needs this the most?)  
    💰 **Revenue Model:** (How does it make money?)  
    📈 **Why It Works:** (Market trends, competitive edge)  
    ✅ **Next Steps:** (How to validate & launch)
    """
    )
    #define the llm model
    model = ChatGroq(groq_api_key=groq_key,
                    model=model,
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2)

    #create document chain
    document_chain = create_stuff_documents_chain(model, business_prompt)

    #create retrival chain
    retrival_chain = create_retrieval_chain(vector_retriever, document_chain)

    #invoke the retrical chain
    response = retrival_chain.invoke({"input": "", "subject": subject})

    return response['answer']