# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download installer from website
```

## Step 2: Pull the Model

```bash
# Pull llama3.2 model (this takes a few minutes)
ollama pull llama3.2

# Start Ollama service
ollama serve
```

Keep this terminal running!

## Step 3: Get Linkup API Key

1. Go to [https://app.linkup.so](https://app.linkup.so)
2. Sign up for a free account
3. Copy your API key

## Step 4: Setup Project

```bash
# Navigate to project directory
cd desktop-agent

# Run setup script
./setup.sh

# Edit .env file and add your API key
nano .env
# Change: LINKUP_API_KEY=your_linkup_api_key_here
# To: LINKUP_API_KEY=<your_actual_key>
```

## Step 5: Test Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Run test script
python test_installation.py
```

All tests should pass ✓

## Step 6: Run the App!

```bash
# Make sure Ollama is still running (ollama serve)
# Then start Streamlit
streamlit run app.py
```

Open browser to [http://localhost:8501](http://localhost:8501)

## 🎉 You're Ready!

Try these example queries:
- "What are the latest AI developments?"
- "List documents in my folder"
- "Research quantum computing breakthroughs"
- "Explain transformer models"

## 🐛 Troubleshooting

### Can't connect to Ollama
```bash
# Make sure Ollama is running
ollama serve

# Check it's working
curl http://localhost:11434/api/tags
```

### Missing API key error
```bash
# Make sure .env file has your key
cat .env | grep LINKUP_API_KEY
```

### Import errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Run [demo.py](demo.py) for a guided demonstration
- Check [Architecture Guide](ARCHITECTURE.md) for technical details

## 💡 Pro Tips

1. **Use Deep Search** for research tasks:
   - "Use deep search to research..."

2. **Reference Context**: 
   - "What did we discuss earlier?"
   - "Tell me more about that"

3. **Multi-Step Tasks**:
   - "List documents, then summarize the first one"

4. **Add Your Documents**:
   - Copy files to `data/documents/`
   - Agent can access them automatically

Happy hacking! 🚀
