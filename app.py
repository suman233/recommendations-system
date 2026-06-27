import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import openai
import os

# Configuration
st.set_page_config(page_title="Sentinel AI Companion", layout="wide")

# Mock Database (In production, use PostgreSQL/Pinecone)
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "task": "Finish Q3 Financial Report", "deadline": datetime.now() + timedelta(hours=5), "status": "Pending", "complexity": "High"},
        {"id": 2, "task": "Pay Electricity Bill", "deadline": datetime.now() + timedelta(days=1), "status": "Pending", "complexity": "Low"}
    ]

def get_ai_recommendation(task, complexity, time_left):
    """The Proactive Logic Layer"""
    prompt = f"""
    User has a task: '{task}' 
    Complexity: {complexity}
    Time remaining: {time_left}
    
    Don't just remind them. Be a proactive companion. 
    1. Suggest a 5-minute micro-action to break the ice.
    2. Offer a 'low-energy' alternative if they are tired.
    3. Identify a potential roadblock.
    Format as a short, punchy proactive nudge.
    """
    try:
        # Replace with your API Key or use Environment Variable
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a proactive productivity agent."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return "⚠️ Connect OpenAI API to see proactive nudges."

# UI Layout
st.title("🛡️ Sentinel: Your Proactive AI Companion")
st.subheader("Moving from reminders to meaningful action.")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("### Your Current Focus")
    for t in st.session_state.tasks:
        time_diff = t['deadline'] - datetime.now()
        hours_left = round(time_diff.total_seconds() / 3600, 1)
        
        with st.expander(f"{t['task']} (Due in {hours_left}h)"):
            st.write(f"**Complexity:** {t['complexity']}")
            if st.button(f"Generate Action Plan for {t['id']}"):
                with st.spinner("AI is analyzing roadblocks..."):
                    rec = get_ai_recommendation(t['task'], t['complexity'], f"{hours_left} hours")
                    st.info(rec)
            if st.button(f"Mark Complete", key=f"btn_{t['id']}"):
                st.success("Task cleared!")

with col2:
    st.write("### AI Proactive Insights")
    st.warning("🤖 **Observation:** You have two high-complexity tasks due today. I've noticed you usually focus best between 2 PM and 4 PM. I will silence non-urgent notifications during that window.")
    
    st.write("---")
    st.write("### Quick Add Task")
    new_t = st.text_input("What's on your mind?")
    if st.button("Add to Sentinel"):
        st.session_state.tasks.append({"id": len(st.session_state.tasks)+1, "task": new_t, "deadline": datetime.now() + timedelta(days=1), "status": "Pending", "complexity": "Medium"})
        st.rerun()