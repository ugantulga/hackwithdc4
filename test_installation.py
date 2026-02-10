#!/usr/bin/env python3
"""
Quick test script to verify Desktop Agent installation
"""
#%%
import os
import sys
from pathlib import Path

print("="*60)
print("DESKTOP INTELLIGENCE AGENT - INSTALLATION TEST")
print("="*60)
print()

# Test 1: Environment
print("📋 Test 1: Environment Setup")
print("-" * 60)

try:
    from linkup import LinkupClient
    client = LinkupClient(api_key="039ce95e-54ba-4cd2-813d-d54dba0b7521")

    response = client.search(
  query="What is Microsoft's revenue and operating income for 2024?",
  depth="standard",
  output_type="searchResults",
  include_images=False,
)

    print(response)
    
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    print(f"✓ Ollama URL: {ollama_url}")
    
except Exception as e:
    print(f"✗ Environment error: {e}")

print()



#%%
# Test 2: Dependencies
print("📦 Test 2: Python Dependencies")
print("-" * 60)

required_packages = [
    ("langchain", "LangChain"),
    ("streamlit", "Streamlit"),
    ("faiss", "FAISS (CPU)"),
    ("sentence_transformers", "Sentence Transformers"),
    ("sqlalchemy", "SQLAlchemy"),
    ("pypdf", "PyPDF"),
    ("docx", "python-docx"),
    ("requests", "Requests"),
]

missing = []
for package, name in required_packages:
    try:
        __import__(package)
        print(f"✓ {name}")
    except ImportError:
        print(f"✗ {name} - NOT INSTALLED")
        missing.append(package)

if missing:
    print()
    print(f"⚠️  Missing packages: {', '.join(missing)}")
    print("   Run: pip install -r requirements.txt")

print()

#%%
# Test 3: Ollama Connection
print("🤖 Test 3: Ollama Connection")
print("-" * 60)

try:
    import requests
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    response = requests.get(f"{ollama_url}/api/tags", timeout=2)
    if response.status_code == 200:
        print("✓ Ollama is running")
        
        models = response.json().get("models", [])
        if models:
            print(f"✓ Available models: {', '.join([m['name'] for m in models])}")
            
            # Check for llama3.2
            if any("llama3.2" in m['name'] for m in models):
                print("✓ llama3.2 model is ready")
            else:
                print("⚠️  llama3.2 not found. Run: ollama pull llama3.2")
        else:
            print("⚠️  No models installed. Run: ollama pull llama3.2")
    else:
        print(f"✗ Ollama returned status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to Ollama")
    print("  → Make sure Ollama is running: ollama serve")
except Exception as e:
    print(f"✗ Ollama error: {e}")

print()

#%%
# Test 4: Directory Structure
print("📁 Test 4: Directory Structure")
print("-" * 60)

directories = [
    "data",
    "data/vector_store",
    "data/documents",
    "agent",
    "tools",
    "memory"
]

for directory in directories:
    path = Path(directory)
    if path.exists():
        print(f"✓ {directory}/")
    else:
        print(f"✗ {directory}/ - NOT FOUND")
        path.mkdir(parents=True, exist_ok=True)
        print(f"  → Created {directory}/")

print()

# Test 5: Import Agent
print("🧪 Test 5: Agent Import")
print("-" * 60)

try:
    sys.path.append(str(Path(__file__).parent))
    from tools.linkup_tool import create_linkup_tools
    from tools.document_tools import create_document_tools
    from memory.local_memory import LocalMemorySystem
    from agent.desktop_agent import DesktopIntelligenceAgent
    
    print("✓ All modules import successfully")
    
    # Try creating tools
    linkup_tools = create_linkup_tools()
    print(f"✓ Created {len(linkup_tools)} Linkup tools")
    
    doc_tools = create_document_tools()
    print(f"✓ Created {len(doc_tools)} document tools")
    
    print("✓ Agent is ready to initialize")
    
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()

print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
print()
print("If all tests passed ✓, you're ready to run:")
print("  streamlit run app.py")
print()
print("If there are errors ✗, fix them following the suggestions above")
print()

# %%
