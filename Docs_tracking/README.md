# 🤖 Desktop Intelligence Agent

An AGI-inspired desktop assistant demonstrating multi-domain intelligence, privacy-first architecture, and autonomous task execution. Built for the hackathon challenge.

## 🌟 Key Features

### Multi-Domain Intelligence
- **Web Search**: Real-time information retrieval via Linkup API
- **Document Processing**: Local PDF, DOCX, TXT analysis
- **Contextual Memory**: Vector search (FAISS) + structured memory (SQLite)
- **Task Automation**: Autonomous planning and execution

### Privacy-First Architecture
- ✅ **Local LLM**: Ollama (llama3.2) runs on your machine
- ✅ **Local Storage**: FAISS vector store + SQLite database
- ✅ **Local Processing**: All documents processed locally
- ⚠️ **External API**: Only Linkup for web search (with privacy controls)

### Agent Capabilities
- Natural language understanding and task decomposition
- Intelligent tool selection and chaining
- Memory-augmented reasoning
- Context awareness across conversations

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Streamlit UI (localhost:8501)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   LangChain ReAct Agent            │
│   - Multi-domain reasoning         │
│   - Tool orchestration             │
│   - Planning & execution           │
└──────────────┬──────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼──────┐    ┌────▼──────────┐
│ Local LLM  │    │ Linkup API    │
│ (Ollama)   │    │ (Web Search)  │
└─────┬──────┘    └───────────────┘
      │
┌─────▼──────────────────────────────┐
│ Local Memory System                │
│ - FAISS (vector embeddings)        │
│ - SQLite (conversation history)    │
│ - Sentence Transformers (local)    │
└────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.ai) installed and running
- [Linkup API key](https://app.linkup.so)

### Installation

1. **Clone and setup**:
```bash
cd desktop-agent
./setup.sh
```

2. **Configure API key**:
```bash
# Edit .env file
nano .env

# Add your Linkup API key:
LINKUP_API_KEY=your_api_key_here
```

3. **Start Ollama** (in separate terminal):
```bash
ollama serve
```

4. **Run the application**:
```bash
source venv/bin/activate
streamlit run app.py
```

5. **Open browser** to `http://localhost:8501`

## 📖 Usage Examples

### Web Search
```
User: "What are the latest developments in quantum computing?"
Agent: [Uses linkup_search] → Returns current information with sources
```

### Document Analysis
```
User: "Summarize the PDF in the documents folder"
Agent: [Uses list_documents + read_pdf] → Provides summary
```

### Multi-Step Task
```
User: "Research Acme Corp and draft an email response"
Agent: 
  1. [linkup_search] Research Acme Corp
  2. [Reasoning] Analyze information
  3. [Generate] Draft professional email
```

### Context Awareness
```
User: "What did we discuss earlier?"
Agent: [Memory search] → Retrieves relevant past conversations
```

## 🛠️ Available Tools

### Web Search (Linkup)
- `linkup_search`: Standard web search
- `linkup_deep_search`: Comprehensive research (slower)

### Document Processing
- `list_documents`: Show available documents
- `read_pdf`: Extract text from PDFs
- `read_docx`: Extract text from Word docs
- `read_text_file`: Read plain text files

## 🧠 Memory System

### Vector Storage (FAISS)
- Semantic search over past conversations
- Local sentence embeddings (MiniLM)
- Persistent storage in `data/vector_store/`

### Structured Memory (SQLite)
- Conversation history
- Document references
- Task logs
- Location: `data/agent_memory.db`

## 🔒 Privacy & Security

### What Stays Local
✅ LLM inference (Ollama)
✅ Document processing
✅ Vector embeddings
✅ Conversation history
✅ All user data

### External Calls
⚠️ Linkup API (web search only)
- Sanitized queries (no PII)
- Source citations included
- User-controlled

### Data Storage
- All data stored in `data/` directory
- SQLite database (plaintext, local)
- FAISS index (binary, local)
- No cloud sync

## 📁 Project Structure

```
desktop-agent/
├── app.py                      # Streamlit UI
├── requirements.txt            # Dependencies
├── setup.sh                    # Setup script
├── .env.template              # Environment template
│
├── agent/
│   └── desktop_agent.py       # Main agent logic
│
├── tools/
│   ├── linkup_tool.py         # Linkup web search
│   └── document_tools.py      # Document processing
│
├── memory/
│   └── local_memory.py        # FAISS + SQLite memory
│
└── data/                      # Local storage (gitignored)
    ├── vector_store/          # FAISS index
    ├── documents/             # User documents
    └── agent_memory.db        # SQLite database
```

## 🎯 Hackathon Requirements Checklist

### Core Requirements
- ✅ **Multi-domain Intelligence**: Web search, documents, memory
- ✅ **Natural Language to Action**: LangChain ReAct agent
- ✅ **Knowledge Transfer**: Shared reasoning across domains
- ✅ **Contextual Memory**: FAISS + SQLite
- ✅ **Autonomous Planning**: ReAct framework with tool use
- ✅ **Privacy-First**: Local LLM and storage

### Linkup Integration (Main Track)
- ✅ **Agentic Search API**: Two search tools (standard + deep)
- ✅ **Intelligent Triggering**: Agent decides when to search
- ✅ **Query Formulation**: Natural language queries
- ✅ **Information Synthesis**: Combines local + web knowledge
- ✅ **Privacy Protection**: Sanitizes queries before API calls

### Technical Stack
- ✅ LangChain for agent orchestration
- ✅ Ollama for local LLM
- ✅ FAISS for vector storage
- ✅ SQLite for structured memory
- ✅ Streamlit for UI

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Linkup API
LINKUP_API_KEY=your_key_here

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Storage
VECTOR_STORE_PATH=./data/vector_store
SQLITE_DB_PATH=./data/agent_memory.db
DOCUMENTS_PATH=./data/documents
```

### Changing the LLM Model
```bash
# Pull different model
ollama pull mistral

# Update .env
OLLAMA_MODEL=mistral
```

## 🐛 Troubleshooting

### "Connection refused" error
```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### "LINKUP_API_KEY not set"
```bash
# Edit .env file
nano .env

# Add your API key
LINKUP_API_KEY=your_actual_key
```

### Slow performance
- Use smaller model: `ollama pull llama3.2:1b`
- Reduce max_iterations in agent config
- Use standard search instead of deep search

### Module import errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 🚧 Future Enhancements

- [ ] Email integration (IMAP)
- [ ] Calendar management
- [ ] Multi-file analysis
- [ ] Custom tool creation interface
- [ ] Voice input/output
- [ ] Mobile app (Electron wrapper)
- [ ] Document OCR support
- [ ] More LLM backends (GPT-4, Claude via API)

## 📊 Performance Notes

### Response Times (Typical)
- Simple query: 2-5 seconds
- Web search: 3-8 seconds  
- Deep search: 10-20 seconds
- Document processing: 1-3 seconds

### Resource Usage
- RAM: ~2-4 GB (with llama3.2)
- CPU: Moderate (during inference)
- Storage: ~5 GB (model + data)

## 🤝 Contributing

This is a hackathon project, but contributions welcome:
1. Fork the repo
2. Create feature branch
3. Submit pull request

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) - Claude and MCP
- [Linkup](https://linkup.so) - Web search API
- [LangChain](https://langchain.com) - Agent framework
- [Ollama](https://ollama.ai) - Local LLM runtime

## 📧 Contact

For questions about this project, please open an issue.

---

Built with ❤️ for the AGI Desktop Agent Hackathon
