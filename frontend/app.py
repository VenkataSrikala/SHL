import streamlit as st
import requests
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="SHL Assessment Finder",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 SHL Assessment Recommender")
st.markdown("Find the perfect SHL assessments for your job requirements")

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Input section
st.subheader("Enter Job Requirements")

input_type = st.radio(
    "Input Type:",
    ["Natural Language Query", "Job Description Text", "Job Description URL"]
)

if input_type == "Natural Language Query":
    query = st.text_input(
        "Query",
        placeholder="e.g., Need Python developer with SQL and problem solving skills"
    )
elif input_type == "Job Description Text":
    query = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here...",
        height=150
    )
else:
    url = st.text_input(
        "Job Description URL",
        placeholder="https://jobs.company.com/data-analyst-role"
    )
    if url:
        st.info("URL parsing not yet implemented. Please use text input.")
        query = ""
    else:
        query = ""

# Settings
col1, col2 = st.columns(2)
with col1:
    num_results = st.slider("Number of recommendations", 5, 15, 10)
with col2:
    balanced = st.checkbox("Balanced recommendations", value=True)

# Recommend button
if st.button("🔍 Find Assessments", type="primary"):
    if not query:
        st.warning("Please enter a query or job description")
    else:
        with st.spinner("Finding best assessments..."):
            try:
                response = requests.post(
                    f"{API_URL}/recommend",
                    json={
                        "query": query,
                        "k": num_results,
                        "balanced": balanced
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("recommended_assessments", [])
                    
                    st.success(f"Found {len(results)} recommendations")
                    
                    # Display results
                    for i, assessment in enumerate(results, 1):
                        with st.expander(f"#{i} - {assessment['name']}", expanded=(i <= 3)):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**Description:** {assessment['description']}")
                                st.markdown(f"**Test Type:** {', '.join(assessment['test_type'])}")
                                if assessment.get('duration'):
                                    st.markdown(f"**Duration:** {assessment['duration']} minutes")
                            
                            with col2:
                                st.markdown(f"**Remote:** {assessment['remote_support']}")
                                st.markdown(f"**Adaptive:** {assessment['adaptive_support']}")
                            
                            st.markdown(f"[View Assessment]({assessment['url']})")
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Make sure the API server is running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This tool uses AI to recommend relevant SHL assessments based on job requirements.
    
    **Features:**
    - Natural language understanding
    - Semantic search
    - Balanced recommendations
    - 377+ assessments
    """)
    
    st.header("API Status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=5)
        if health.status_code == 200:
            st.success("✅ API Online")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")
