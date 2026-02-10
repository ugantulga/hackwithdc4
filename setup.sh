#!/bin/bash

echo "=================================="
echo "Desktop Intelligence Agent Setup"
echo "=================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Check if Ollama is installed
echo ""
echo "🔍 Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    ollama_version=$(ollama --version 2>&1)
    echo "   ✓ Ollama is installed: $ollama_version"
else
    echo "   ⚠️  Ollama not found!"
    echo "   Please install Ollama from: https://ollama.ai"
    echo "   Then run: ollama pull llama3.2"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/vector_store
mkdir -p data/documents
echo "   ✓ Created data/vector_store"
echo "   ✓ Created data/documents"

# Create .env file if it doesn't exist
echo ""
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.template .env
    echo "   ✓ Created .env file"
    echo ""
    echo "   ⚠️  IMPORTANT: Edit .env and add your LINKUP_API_KEY"
    echo "   Get your API key from: https://app.linkup.so"
else
    echo "   ✓ .env file already exists"
fi

# Check if Ollama is running and pull model
echo ""
echo "🤖 Checking Ollama model..."
if command -v ollama &> /dev/null; then
    # Try to pull the model
    echo "   Pulling llama3.2 model (this may take a while)..."
    ollama pull llama3.2 2>&1 | grep -v "^$"
    
    if [ $? -eq 0 ]; then
        echo "   ✓ Model ready"
    else
        echo "   ⚠️  Could not pull model. Make sure Ollama is running."
        echo "   Run: ollama serve"
    fi
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your LINKUP_API_KEY"
echo "2. Make sure Ollama is running: ollama serve"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Run the app: streamlit run app.py"
echo ""
echo "For more information, see README.md"
echo ""
