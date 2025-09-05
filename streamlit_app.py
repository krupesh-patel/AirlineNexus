import streamlit as st
import os
import sys
from datetime import datetime
import json
import time

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from airline_nexus import airline_agent

# Page configuration
st.set_page_config(
    page_title="AirlineNexus - AI Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.2);
    }
    
    .welcome-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .agent-card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .message-bubble {
        max-width: 85%;
        padding: 1.25rem;
        border-radius: 1.25rem;
        margin: 0.75rem 0;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.5rem;
    }
    
    .assistant-bubble {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 0.5rem;
    }
    
    .error-bubble {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 0.5rem;
    }
    
    .thinking-indicator {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 1rem;
        text-align: center;
        color: #6b7280;
        margin: 1rem 0;
        border: 2px dashed #d1d5db;
    }
    
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .example-button {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border: 1px solid #d1d5db;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin: 0.25rem;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }
    
    .example-button:hover {
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
        transform: scale(1.02);
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 0.75rem;
        margin-bottom: 2rem;
    }
    
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #6b7280;
        font-style: italic;
    }
    
    .dot {
        width: 8px;
        height: 8px;
        background-color: #6b7280;
        border-radius: 50%;
        animation: bounce 1.4s infinite;
    }
    
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False

def create_typing_indicator():
    return """
    <div class="typing-indicator">
        🤖 AirlineNexus is thinking
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
    """

# Enhanced Sidebar
with st.sidebar:
    # Logo section - more compact
    st.markdown("""
    <div class="sidebar-logo">
        <h3 style="color: white; margin: 0; font-size: 1.5rem;">✈️ AirlineNexus</h3>
        <p style="color: #bfdbfe; margin: 0.3rem 0 0 0; font-size: 0.8rem;">Aviation intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Session stats - moved to top
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        conversations = len(st.session_state.messages)//2 if len(st.session_state.messages) > 0 else 0
        st.markdown(f"""
        <div style="background: white; padding: 0.75rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e5e7eb;">
            <h4 style="color: #3b82f6; margin: 0; font-size: 1.2rem;">{conversations}</h4>
            <p style="margin: 0; font-size: 0.75rem; color: #6b7280;">Chats</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f"""
        <div style="background: white; padding: 0.75rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e5e7eb;">
            <h4 style="color: #10b981; margin: 0; font-size: 1.2rem;">{user_messages}</h4>
            <p style="margin: 0; font-size: 0.75rem; color: #6b7280;">Questions</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    # Clear conversation button - more compact
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.session_state.processing = False
        st.success("Conversation cleared!")
        time.sleep(0.5)
        st.rerun()
    
    # Agents section - more compact
    st.markdown("---")
    st.markdown("### 🤖 AI Agents")
    
    agents_info = [
        ("🛫", "Flight", "#3b82f6"),
        ("📋", "Policy", "#10b981"),
        ("🎧", "Support", "#f59e0b"),
        ("💬", "General", "#8b5cf6")
    ]
    
    for icon, agent_name, color in agents_info:
        st.markdown(f"""
        <div style="background: white; padding: 0.5rem 0.75rem; border-radius: 0.5rem; margin: 0.3rem 0; border-left: 3px solid {color}; border: 1px solid #e5e7eb;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                <strong style="color: {color}; font-size: 0.9rem;">{agent_name} Agent</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Example queries - moved to bottom
    st.markdown("---")
    st.markdown("### 💡 Try Examples")
    
    example_queries = [
        ("🛫", "I want to book a business class flight for 2 people from London to Toronto on September 25, 2025"),
        ("📋", "I cancelled my flight, but I didn't get a refund"),
        ("❓", "Can I carry 20kg baggage?"),
        ("🍽️", "If flight delay then meal will be provided?"),
    ]
    
    for icon, query in example_queries:
        if st.button(f"{icon} {query}", key=f"example_{hash(query)}", use_container_width=True):
            # Set processing state first
            st.session_state.processing = True
            st.session_state.messages.append({"role": "user", "content": query, "timestamp": datetime.now()})
            st.rerun()
    
    # Footer - more compact
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #9ca3af; font-size: 0.7rem;">
        <p style="margin: 0;">🚀 Multi-Agent AI</p>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">✈️ AirlineNexus<br><span style="font-size: 1.2rem; font-weight: 400;">Aviation intelligence. The secret to seamless travel.</span></div>', unsafe_allow_html=True)

# Welcome section (only show if no messages)
if not st.session_state.messages:
    # Feature grid
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🛫</div>
            <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">Flight Services</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Search flights, manage bookings, check status & modifications</p>
        </div>
        <div class="feature-card">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📋</div>
            <h4 style="color: #10b981; margin-bottom: 0.5rem;">Policy Information</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Get answers about baggage, cancellation & travel policies</p>
        </div>
        <div class="feature-card">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎧</div>
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">Support Services</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Handle complex issues, create tickets & get assistance</p>
        </div>
        <div class="feature-card">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
            <h4 style="color: #8b5cf6; margin-bottom: 0.5rem;">General Help</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Ask general questions & get travel information</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat interface
chat_container = st.container()

# Display chat messages with enhanced styling
if st.session_state.messages:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for i, message in enumerate(st.session_state.messages):
        timestamp = message.get("timestamp", datetime.now()).strftime("%I:%M %p") if "timestamp" in message else ""
        
        if message["role"] == "user":
            st.markdown(f'''
            <div class="message-bubble user-bubble">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <strong>👤 You</strong>
                    <span style="margin-left: auto; font-size: 0.75rem; opacity: 0.8;">{timestamp}</span>
                </div>
                <div>{message["content"]}</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="message-bubble assistant-bubble">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <strong>🤖 AirlineNexus</strong>
                    <span style="margin-left: auto; font-size: 0.75rem; opacity: 0.8;">{timestamp}</span>
                </div>
                <div>{message["content"]}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Processing indicator
if st.session_state.processing:
    st.markdown(create_typing_indicator(), unsafe_allow_html=True)

# Chat input with enhanced placeholder
input_placeholder = "✈️ Ask about flights, policies, support, or general travel questions..."
if prompt := st.chat_input(input_placeholder, key="chat_input"):
    # Add user message with timestamp
    user_message = {
        "role": "user", 
        "content": prompt, 
        "timestamp": datetime.now()
    }
    st.session_state.messages.append(user_message)
    st.session_state.processing = True
    st.rerun()

# Process user input when in processing state
if st.session_state.processing and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    latest_prompt = st.session_state.messages[-1]["content"]
    
    # Show processing status
    with st.status("🤖 Processing your request...", expanded=True) as status:
        st.write("🧠 Aviation intelligence. The secret to seamless travel")
        
        try:
            # Get response from the airline agent
            response = airline_agent(latest_prompt)
            response_content = str(response)
            
            st.write("✅ Response generated!")
            status.update(label="✅ Complete!", state="complete")
            
            # Add assistant response with timestamp
            assistant_message = {
                "role": "assistant", 
                "content": response_content,
                "timestamp": datetime.now()
            }
            st.session_state.messages.append(assistant_message)
            
        except Exception as e:
            st.write("❌ Error occurred!")
            status.update(label="❌ Failed!", state="error")
            
            error_message = f"I apologize, but I encountered an error while processing your request. Please try again or rephrase your question.\n\nError details: {str(e)}"
            assistant_message = {
                "role": "assistant", 
                "content": error_message,
                "timestamp": datetime.now(),
                "error": True
            }
            st.session_state.messages.append(assistant_message)
        
        finally:
            # Clear processing state
            st.session_state.processing = False
            # Wait a moment to show the status update
            time.sleep(1)
            st.rerun()
