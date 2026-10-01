import streamlit as st
import json
from categories import CATEGORIES
from agent1_classifier import classify_query
from agent2_source_finder import find_sources
from agent3_researcher import gather_information
from agent4_finalizer import generate_final_response

# Page configuration
st.set_page_config(
    page_title="Pakistan Government Service Navigator",
    page_icon="🇵🇰",
    layout="wide"
)

# Custom Styling for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1A365D;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4A5568;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #1A365D;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
    }
    .category-box {
        background-color: #F7FAFC;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #2B6CB0;
    }
</style>
""", unsafe_allow_html=True)

# Application Layout
col_main, col_sidebar = st.columns([2.2, 1])

with col_sidebar:
    st.markdown("### 📋 Supported Services")
    st.caption("16 Service Categories")
    for cat_name, subcats in CATEGORIES.items():
        with st.expander(cat_name):
            for sub in subcats:
                st.markdown(f"• {sub}")

with col_main:
    st.markdown('<div class="main-header">Pakistan Government Service Navigator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">AI-Powered Multi-Agent Information System for Government, Public, Utility, and Telecom Services</div>',
        unsafe_allow_html=True
    )
    
    st.info(
        "👋 **Welcome!** Describe what service you need in simple English. "
        "Our AI agents will analyze your request, search official sources, and provide step-by-step guidance."
    )
    
    user_query = st.text_area(
        "Describe your question here:",
        placeholder="e.g., 'I lost my identity card and need to get a new one' or 'How do I transfer my vehicle ownership?'",
        height=100
    )
    
    submit_btn = st.button("Search Navigator 🔎")
    
    if submit_btn and user_query.strip():
        # Agent Execution Workflow
        status_box = st.status("🚀 Processing request through AI Agents...", expanded=True)
        
        try:
            # Step 1: Agent 1 Classifier
            status_box.write("🧠 **Agent 1:** Analyzing semantic meaning and classifying category...")
            a1_res = classify_query(user_query)
            
            if a1_res.get("status") == "OUT_OF_SCOPE":
                status_box.update(label="Process completed", state="complete", expanded=False)
                st.warning(
                    "I'm sorry, I can't help with this request because I have access to limited information. "
                    "Please ask a query related to one of the categories listed on the right side of the interface."
                )
            
            elif a1_res.get("status") == "CLARIFICATION_REQUIRED":
                status_box.update(label="Clarification needed", state="complete", expanded=False)
                st.info(f"❓ {a1_res.get('clarification_question', 'Could you please specify which document or service you need assistance with?')}")
                
            elif a1_res.get("status") == "IN_SCOPE":
                category = a1_res.get("category")
                service = a1_res.get("service")
                
                status_box.write(f"✅ Identified Category: **{category}** ➔ **{service}**")
                
                # Step 2: Agent 2 Source Finder
                status_box.write("🌐 **Agent 2:** Searching web and finding official authority sources...")
                a2_res = find_sources(user_query, category, service)
                
                # Step 3: Agent 3 Researcher
                status_box.write("🔍 **Agent 3:** Gathering structured facts and procedure requirements...")
                a3_res = gather_information(user_query, category, service, a2_res)
                
                # Step 4: Agent 4 Finalizer
                status_box.write("📝 **Agent 4:** Finalizing user-friendly response...")
                final_answer = generate_final_response(user_query, a3_res)
                
                status_box.update(label="Answer generated successfully!", state="complete", expanded=False)
                
                # Render Final Output
                st.markdown("### 🎯 Guidance & Information")
                st.markdown(final_answer)
                
                # Hackathon Inspection Section
                st.markdown("---")
                with st.expander("🛠️ Hackathon Inspection: AI Multi-Agent Processing Details"):
                    st.json({
                        "Agent 1 (Classifier)": a1_res,
                        "Agent 2 (Sources Found)": a2_res.get("sources", []),
                        "Agent 3 (Gathered Facts)": a3_res
                    })
                    
        except Exception as e:
            status_box.update(label="Error occurred", state="error", expanded=True)
            st.error(f"An unexpected error occurred during processing: {str(e)}")
            st.caption("Please verify that your GROQ_API_KEY is properly configured in Streamlit Secrets.")
