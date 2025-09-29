# 📄 Autogen ArXiv Finder

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-orange)](https://streamlit.io/)  
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-blueviolet)](https://openai.com/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Autogen ArXiv Finder** is an AI-powered literature review tool that automates the discovery, summarization, and presentation of research papers from [arXiv](https://arxiv.org/). Leveraging OpenAI GPT models and Autogen agents, it provides structured summaries, interactive paper cards, and multiple download formats, streamlining academic research workflows.  

![Preview GIF](https://i.gifer.com/YCZH.gif)

---

## 🔹 Features

- **Automated Literature Search**: Generates optimal arXiv queries for any research topic.  
- **Structured Summaries**: Displays title, authors, publication date, 2-line summary, and PDF link for each paper.  
- **Interactive UI**: Elegant Streamlit interface with floating cards and hover animations.  
- **Multi-format Downloads**: Export literature reviews in Markdown, PDF, or Word.  
- **Async AI Processing**: Real-time streaming of results.  
- **Full Paper Access**: Clickable PDF links to view complete research articles.  

---

## 🔹 Technologies Used

- **Python 3.9+**  
- **[Streamlit](https://streamlit.io/)** – Interactive frontend  
- **[Autogen AgentChat](https://github.com/your-repo)** – AI agents for search and summarization  
- **[OpenAI GPT Models](https://openai.com/)** – NLP backend  
- **[arXiv API](https://arxiv.org/help/api/index)** – Research paper source  
- **FPDF & python-docx** – PDF and Word export  

---

## 🔹 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/autogen-arxiv-finder.git
cd autogen-arxiv-finder
---
##

conda create -n autogen_arxiv python=3.9 -y
conda activate autogen_arxiv
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key_here"  # Linux/macOS
setx OPENAI_API_KEY "your_api_key_here"     # Windows
streamlit run app.py


