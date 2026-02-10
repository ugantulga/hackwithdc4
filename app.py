"""
Streamlit UI for Desktop Intelligence Agent
Privacy-first local web interface
"""
import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from agent.desktop_agent import DesktopIntelligenceAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="Desktop Intelligence Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .tool-badge {
        background-color: #E3F2FD;
        padding: 0.3rem 0.6rem;
        border-radius: 0.3rem;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.85rem;
    }
    .privacy-badge {
        background-color: #C8E6C9;
        padding: 0.3rem 0.6rem;
        border-radius: 0.3rem;
        font-weight: bold;
        color: #2E7D32;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_agent():
    """Load agent (cached to avoid reloading)"""
    try:
        agent = DesktopIntelligenceAgent(
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            verbose=False  # Disable verbose for cleaner UI
        )
        return agent, None
    except Exception as e:
        return None, str(e)


def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<div class="main-header">🤖 Desktop Intelligence Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AGI-Inspired Multi-Domain Assistant with Privacy-First Architecture</div>', unsafe_allow_html=True)
    
    # Privacy badge
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            '<div style="text-align: center;"><span class="privacy-badge">🔒 100% Local Processing (except web search)</span></div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent_loaded" not in st.session_state:
        with st.spinner("🔄 Initializing agent... This may take a moment."):
            agent, error = load_agent()
            if error:
                st.error(f"❌ Failed to initialize agent: {error}")
                st.info("💡 Make sure Ollama is running: `ollama serve`")
                st.info("💡 Check your .env file has LINKUP_API_KEY set")
                st.stop()
            else:
                st.session_state.agent = agent
                st.session_state.agent_loaded = True
                st.success("✅ Agent initialized successfully!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Agent info
        st.subheader("Agent Status")
        if st.session_state.agent_loaded:
            st.success("🟢 Active")
            
            agent = st.session_state.agent
            
            # Show available tools
            st.subheader("🛠️ Available Tools")
            for tool in agent.tools:
                st.markdown(f'<span class="tool-badge">{tool.name}</span>', unsafe_allow_html=True)
            
            # Memory stats
            st.subheader("🧠 Memory")
            try:
                recent = agent.memory.get_recent_conversations(limit=5)
                st.metric("Conversations Stored", len(recent))
            except:
                st.metric("Conversations Stored", "N/A")
            
            # Actions
            st.subheader("🎯 Actions")
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            
            if st.button("💾 Save Memory", use_container_width=True):
                agent.memory.save()
                st.success("Memory saved!")
            
            # System info
            st.markdown("---")
            st.subheader("📊 System Info")
            st.text(f"LLM: {os.getenv('OLLAMA_MODEL', 'llama3.2')}")
            st.text(f"Embeddings: Local (MiniLM)")
            st.text(f"Vector DB: FAISS")
            st.text(f"Memory: SQLite")
        else:
            st.error("🔴 Not initialized")
        
        # Links
        st.markdown("---")
        st.markdown("**📚 Resources**")
        st.markdown("- [GitHub](#)")
        st.markdown("- [Documentation](#)")
        st.markdown("- [Linkup API](https://linkup.so)")
    
    # Main chat interface
    st.header("💬 Chat")
    
    # Display example queries
    if not st.session_state.messages:
        st.info("👋 Welcome! Try asking me to:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌐 Search for latest AI news", use_container_width=True):
                st.session_state.example_query = "What are the latest developments in AI?"
                st.rerun()
            
            if st.button("📄 List available documents", use_container_width=True):
                st.session_state.example_query = "List all documents in the documents folder"
                st.rerun()
        
        with col2:
            if st.button("🔍 Research a company", use_container_width=True):
                st.session_state.example_query = "Research information about Anthropic"
                st.rerun()
            
            if st.button("💡 Explain a concept", use_container_width=True):
                st.session_state.example_query = "Explain how transformer models work"
                st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show tools used if available
            if "tools" in message and message["tools"]:
                st.caption(f"🛠️ Tools used: {', '.join(message['tools'])}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    result = st.session_state.agent.run(prompt)
                    response = result["output"]
                    tools_used = result.get("tools_used", [])
                    
                    st.markdown(response)
                    
                    if tools_used:
                        st.caption(f"🛠️ Tools used: {', '.join(tools_used)}")
                    
                    # Add to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "tools": tools_used
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "tools": []
                    })
    
    # Handle example queries
    if "example_query" in st.session_state:
        query = st.session_state.example_query
        del st.session_state.example_query
        
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #888; font-size: 0.9rem;">'
        '🔒 Privacy-First | 🏠 Local Processing | 🌐 Web Search via Linkup'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
