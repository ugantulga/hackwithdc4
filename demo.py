#!/usr/bin/env python3
"""
Demo Script - Showcases Desktop Intelligence Agent Capabilities
Perfect for hackathon presentations!
"""
import os
import sys
from pathlib import Path
from time import sleep
from dotenv import load_dotenv

# Setup path
sys.path.append(str(Path(__file__).parent))

from agent.desktop_agent import DesktopIntelligenceAgent


def print_banner(text):
    """Print a nice banner"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_section(text):
    """Print section header"""
    print("\n" + "-"*70)
    print(f">>> {text}")
    print("-"*70 + "\n")


def demo_web_search(agent):
    """Demo 1: Web search capabilities"""
    print_banner("DEMO 1: WEB SEARCH WITH LINKUP")
    
    print("Scenario: User needs current information about AI developments\n")
    
    query = "What are the latest breakthroughs in large language models in 2024?"
    
    print(f"USER: {query}\n")
    print("AGENT: [Thinking...]\n")
    
    result = agent.run(query)
    
    print(f"RESPONSE:\n{result['output']}\n")
    
    if result['tools_used']:
        print(f"🛠️  Tools Used: {', '.join(result['tools_used'])}")
    
    print("\n✓ Demonstrates: Real-time web knowledge retrieval with source citations")


def demo_context_awareness(agent):
    """Demo 2: Context awareness and memory"""
    print_banner("DEMO 2: CONTEXT AWARENESS & MEMORY")
    
    print("Scenario: Multi-turn conversation with context retention\n")
    
    # First query
    query1 = "What is transformer architecture in deep learning?"
    print(f"USER: {query1}\n")
    print("AGENT: [Searching and reasoning...]\n")
    
    result1 = agent.run(query1)
    print(f"RESPONSE:\n{result1['output'][:300]}...\n")
    
    sleep(1)
    
    # Follow-up query (tests memory)
    print_section("Follow-up Question")
    
    query2 = "Who invented that architecture?"
    print(f"USER: {query2}\n")
    print("AGENT: [Checking memory and searching...]\n")
    
    result2 = agent.run(query2)
    print(f"RESPONSE:\n{result2['output']}\n")
    
    print("✓ Demonstrates: Context awareness, memory retrieval, reference resolution")


def demo_multi_domain(agent):
    """Demo 3: Multi-domain intelligence"""
    print_banner("DEMO 3: MULTI-DOMAIN INTELLIGENCE")
    
    print("Scenario: Task requires both document access and web search\n")
    
    query = "List the documents I have, and then search for recent papers on the main topic"
    
    print(f"USER: {query}\n")
    print("AGENT: [Planning multi-step task...]\n")
    
    result = agent.run(query)
    
    print(f"RESPONSE:\n{result['output']}\n")
    
    if result['tools_used']:
        print(f"🛠️  Tools Used: {', '.join(result['tools_used'])}")
    
    print("\n✓ Demonstrates: Multi-domain reasoning, tool chaining, autonomous planning")


def demo_research_task(agent):
    """Demo 4: Complex research task"""
    print_banner("DEMO 4: RESEARCH & SYNTHESIS")
    
    print("Scenario: Research a company before drafting a response\n")
    
    query = "Research Anthropic (the AI company) and tell me their main products"
    
    print(f"USER: {query}\n")
    print("AGENT: [Conducting research...]\n")
    
    result = agent.run(query)
    
    print(f"RESPONSE:\n{result['output']}\n")
    
    if result['tools_used']:
        print(f"🛠️  Tools Used: {', '.join(result['tools_used'])}")
    
    print("\n✓ Demonstrates: Information gathering, synthesis, structured response")


def demo_privacy(agent):
    """Demo 5: Privacy features"""
    print_banner("DEMO 5: PRIVACY-FIRST ARCHITECTURE")
    
    print("Key Privacy Features:\n")
    
    print("1. LOCAL LLM (Ollama)")
    print("   ✓ All reasoning happens on your machine")
    print("   ✓ No API calls to OpenAI, Anthropic, etc.")
    print("   ✓ Model: llama3.2\n")
    
    print("2. LOCAL STORAGE")
    print("   ✓ FAISS vector store (local files)")
    print("   ✓ SQLite database (local file)")
    print("   ✓ All conversation history stays local\n")
    
    print("3. LOCAL DOCUMENT PROCESSING")
    print("   ✓ PDFs processed locally (pypdf)")
    print("   ✓ DOCX processed locally (python-docx)")
    print("   ✓ No documents sent to external services\n")
    
    print("4. CONTROLLED EXTERNAL ACCESS")
    print("   ⚠️  Only Linkup API for web search")
    print("   ✓ Queries sanitized (no PII)")
    print("   ✓ User controls when to search\n")
    
    # Show memory location
    print("5. DATA LOCATION")
    print(f"   Vector Store: {agent.memory.vector_store_path}")
    print(f"   Database: {agent.memory.sqlite_db_path}")
    print(f"   → You control your data!\n")
    
    print("✓ Demonstrates: Privacy-first design, local-first architecture")


def main():
    """Run the demo"""
    load_dotenv()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🤖 DESKTOP INTELLIGENCE AGENT DEMO 🤖                ║
║                                                              ║
║            AGI-Inspired Multi-Domain Assistant              ║
║         with Privacy-First Local Architecture               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\nInitializing agent...\n")
    
    try:
        agent = DesktopIntelligenceAgent(
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            verbose=False  # Clean output for demo
        )
        
        print("✅ Agent initialized successfully!\n")
        sleep(1)
        
        # Run demos
        print("\n🎬 Starting Demonstration...\n")
        sleep(1)
        
        # Demo 1: Web Search
        demo_web_search(agent)
        input("\n\nPress Enter to continue to Demo 2...")
        
        # Demo 2: Context Awareness
        demo_context_awareness(agent)
        input("\n\nPress Enter to continue to Demo 3...")
        
        # Demo 3: Multi-Domain
        demo_multi_domain(agent)
        input("\n\nPress Enter to continue to Demo 4...")
        
        # Demo 4: Research
        demo_research_task(agent)
        input("\n\nPress Enter to continue to Demo 5...")
        
        # Demo 5: Privacy
        demo_privacy(agent)
        
        # Wrap up
        print_banner("DEMO COMPLETE!")
        
        print("""
Key Takeaways:
  ✓ Multi-domain intelligence (web search, documents, memory)
  ✓ Autonomous planning and tool use
  ✓ Context awareness and memory
  ✓ Privacy-first local architecture
  ✓ Linkup integration for real-time knowledge
  ✓ Natural language interface
        
Hackathon Requirements Met:
  ✅ Multi-domain reasoning
  ✅ Natural language to action
  ✅ Knowledge transfer
  ✅ Contextual memory
  ✅ Autonomous planning
  ✅ Privacy-first design
  ✅ Linkup API integration
        
Technology Stack:
  🔧 LangChain (agent framework)
  🤖 Ollama (local LLM)
  🌐 Linkup (web search API)
  💾 FAISS (vector storage)
  🗄️  SQLite (structured memory)
  🎨 Streamlit (web UI)
        """)
        
        print("\n" + "="*70)
        print("Thank you for watching!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check .env file has LINKUP_API_KEY set")
        print("3. Run: python test_installation.py")
        print()


if __name__ == "__main__":
    main()
