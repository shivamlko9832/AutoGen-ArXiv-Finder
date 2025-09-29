# app.py
import streamlit as st
import asyncio
from typing import List, Dict
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
import os
import arxiv
import json
import textwrap

# ==========================
# Backend Setup
# ==========================
openai_brain = OpenAIChatCompletionClient(
    model='gpt-4o', 
    api_key=os.getenv('OPENAI_API_KEY')
)

def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    papers: List[Dict] = []
    for result in client.results(search):
        paper = {
            'title': result.title,
            'authors': [a.name for a in result.authors],
            'published': result.published.strftime('%Y-%m-%d'),
            'summary': result.summary,
            'pdf_url': result.pdf_url,
        }
        papers.append(paper)
    return papers

# Agents
arxiv_researcher_agent = AssistantAgent(
    name="arxiv_search_agent",
    description="Create arXiv queries and retrieves candidate papers from arXiv",
    model_client=openai_brain,
    tools=[arxiv_search],
    system_message=(
        "You are an expert research assistant. "
        "When given a research topic by the user, create the most effective arXiv query "
        "and call the provided tool. "
        "Always fetch enough papers so that the requested number of relevant papers can be selected. "
        "Return the papers as a JSON array of objects with these fields: "
        "title, authors (list), published (YYYY-MM-DD), summary (full abstract), pdf_url. "
        "Do not include any explanations or extra text."
    ),
)


summarizer_agent = AssistantAgent(
    name="summarizer_agent",
    description="An agent which summarizes the result",
    model_client=openai_brain,
    system_message=(
        "You are an expert researcher and summarizer. "
        "When you receive a JSON array of papers, output a JSON array with exactly these fields for each paper:\n"
        "- title\n"
        "- authors (list)\n"
        "- published (YYYY-MM-DD)\n"
        "- summary (max 50 words)\n"
        "- pdf_url\n\n"
        "Do not include any explanations, markdown formatting, or extra text. "
        "Ensure summaries are concise, each ~50 words, and output valid JSON only."
    ),
)


team = RoundRobinGroupChat(
    participants=[arxiv_researcher_agent, summarizer_agent],
    max_turns=2
)

# ==========================
# Streamlit UI
# ==========================
st.markdown("<h1 style='text-align:center; color:blue;'>📄 AutoGen Arxiv Finder</h1>", unsafe_allow_html=True)
st.set_page_config(
    page_title="AutoGen Arxiv Finder",
    page_icon="🔍📄",
    layout="wide"
)



# Gradient Background + CSS Animations
st.markdown("""
<style>
.paper-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    transition: transform 0.2s;
}
.paper-card:hover {
    transform: scale(1.02);
}
.paper-title {
    font-size: 1.3rem;
    font-weight: bold;
    color: #1E3C72;
}
.paper-meta {
    font-size: 0.9rem;
    color: #555;
    margin-bottom: 10px;
}
.paper-summary {
    font-size: 1rem;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# Floating Header
st.markdown("<div class='floating-text'>📄 Autogen Literature Review Tool</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:16px; color:#fff;'>Enter a research topic and get a concise literature review from arXiv</p>", unsafe_allow_html=True)

# ==========================
# Sidebar
# ==========================
st.sidebar.markdown("<div class='sidebar-title'>📝 Instructions</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
- Enter the research topic in the input box.
- Select the number of papers you want in your review.
- Click 'Generate Literature Review' to run the AI agents.
- While generating, a GIF loader will appear.
- Each paper is shown in a floating card.
- Download the review as Markdown using the button below.
""")
st.sidebar.markdown("<div class='sidebar-title'>💡 Tips</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
- Use concise, specific topics for better results.
- The agents fetch 5x papers internally to pick the most relevant ones.
- Ensure your OPENAI_API_KEY is set in the environment.
""")
st.sidebar.markdown("<div class='sidebar-title'>📌 Credits</div>", unsafe_allow_html=True)
st.sidebar.markdown("Developed by **Shivam Kumar** | Powered by Autogen & OpenAI")

# ==========================
# Main Inputs
# ==========================
topic = st.text_input("🔍 Enter your research topic:", "")
num_papers = st.slider("Select number of papers to include:", min_value=1, max_value=10, value=5)
start_button = st.button("🚀 Generate Literature Review")
output_container = st.empty()

# Async function
async def run_team(task: str):
    result_text = ""
    async for msg in team.run_stream(task=task):
        # Extract text safely
        if hasattr(msg, "content"):
            text = msg.content
        else:
            text = str(msg)

        # Handle case where text is a list
        if isinstance(text, list):
            text = "\n".join(map(str, text))

        result_text += text + "\n\n"
        output_container.markdown(result_text)

    return result_text

# ==========================

if start_button and topic.strip():
    # GIF loader animation
    st.markdown("<div style='text-align:center;'><img src='https://i.gifer.com/YCZH.gif' width='100'></div>", unsafe_allow_html=True)
    task = f"Conduct a literature review on the topic - {topic} and return exactly {num_papers} papers."
    result = asyncio.run(run_team(task))
    
    st.success("✅ Literature review generated successfully!")
    st.markdown("---")
    st.markdown("### 📄 Literature Review Output")

    # Split papers into cards
    for paper_block in result.split("\n\n"):
        if paper_block.strip():
            st.markdown(f"<div class='paper-card'>{paper_block}</div>", unsafe_allow_html=True)

    # Download Button
    st.download_button(
        label="📥 Download as Markdown",
        data=result,
        file_name=f"{topic.replace(' ','_')}_literature_review.md",
        mime="text/markdown"
    )

# ==========================
# Footer with Branding
# ==========================
st.markdown(
    "<footer>© 2025 Shivam Kumar | Built with Streamlit & Autogen</footer>", 
    unsafe_allow_html=True
)
