"""
Local Memory System
Combines vector storage (FAISS) and structured memory (SQLite)
"""
import os
import json
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
    VECTOR_AVAILABLE = True
except ImportError:
    VECTOR_AVAILABLE = False
    print("Warning: FAISS or sentence-transformers not available")


class LocalMemorySystem:
    """
    Privacy-first local memory system combining:
    - Vector storage (FAISS) for semantic search
    - Structured storage (SQLite) for conversation history
    """
    
    def __init__(
        self,
        vector_store_path: str = "./data/vector_store",
        sqlite_db_path: str = "./data/agent_memory.db",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        self.vector_store_path = Path(vector_store_path)
        self.sqlite_db_path = Path(sqlite_db_path)
        
        # Create directories
        self.vector_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.sqlite_db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding model (local)
        self.embedding_model_name = embedding_model
        if VECTOR_AVAILABLE:
            self.embedder = SentenceTransformer(embedding_model)
            self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
        else:
            self.embedder = None
            self.embedding_dim = 384  # default for MiniLM
        
        # Initialize or load FAISS index
        self.index = self._load_or_create_index()
        
        # Initialize SQLite database
        self._init_database()
        
        # In-memory store for metadata
        self.metadata_store: List[Dict[str, Any]] = []
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create new one"""
        if not VECTOR_AVAILABLE:
            return None
        
        index_file = self.vector_store_path / "faiss.index"
        
        if index_file.exists():
            try:
                index = faiss.read_index(str(index_file))
                print(f"Loaded existing FAISS index with {index.ntotal} vectors")
                
                # Load metadata
                metadata_file = self.vector_store_path / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        self.metadata_store = json.load(f)
                
                return index
            except Exception as e:
                print(f"Error loading index: {e}. Creating new one.")
        
        # Create new index
        index = faiss.IndexFlatL2(self.embedding_dim)  # L2 distance
        print(f"Created new FAISS index (dim={self.embedding_dim})")
        return index
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        
        # Conversation history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_message TEXT NOT NULL,
                agent_response TEXT NOT NULL,
                tools_used TEXT,
                metadata TEXT
            )
        """)
        
        # Document references table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                file_name TEXT NOT NULL,
                file_type TEXT,
                processed_date TEXT,
                summary TEXT
            )
        """)
        
        # Task/action history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                task_description TEXT NOT NULL,
                status TEXT,
                result TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"Initialized SQLite database at {self.sqlite_db_path}")
    
    def add_conversation(
        self,
        user_message: str,
        agent_response: str,
        tools_used: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Store a conversation turn in both vector store and SQLite
        
        Returns:
            Conversation ID
        """
        timestamp = datetime.now().isoformat()
        
        # Store in SQLite
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (timestamp, user_message, agent_response, tools_used, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            timestamp,
            user_message,
            agent_response,
            json.dumps(tools_used) if tools_used else None,
            json.dumps(metadata) if metadata else None
        ))
        
        conv_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Add to vector store for semantic search
        if VECTOR_AVAILABLE and self.embedder:
            combined_text = f"User: {user_message}\nAgent: {agent_response}"
            self._add_to_vector_store(combined_text, {
                "type": "conversation",
                "id": conv_id,
                "timestamp": timestamp
            })
        
        return conv_id
    
    def _add_to_vector_store(self, text: str, metadata: Dict):
        """Add text embedding to FAISS index"""
        if not VECTOR_AVAILABLE or not self.embedder:
            return
        
        # Generate embedding
        embedding = self.embedder.encode([text])[0]
        embedding = np.array([embedding], dtype='float32')
        
        # Add to index
        self.index.add(embedding)
        
        # Store metadata
        self.metadata_store.append(metadata)
        
        # Save periodically
        if len(self.metadata_store) % 10 == 0:
            self.save()
    
    def semantic_search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Perform semantic search over stored conversations and documents
        
        Args:
            query: Search query
            k: Number of results to return
        
        Returns:
            List of relevant results with metadata
        """
        if not VECTOR_AVAILABLE or not self.embedder:
            return []
        
        # Generate query embedding
        query_embedding = self.embedder.encode([query])[0]
        query_embedding = np.array([query_embedding], dtype='float32')
        
        # Search
        if self.index.ntotal == 0:
            return []
        
        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        # Retrieve metadata
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata_store):
                result = self.metadata_store[idx].copy()
                result['similarity_score'] = float(1 / (1 + dist))  # Convert distance to similarity
                results.append(result)
        
        return results
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history from SQLite"""
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, user_message, agent_response, tools_used
            FROM conversations
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversations.append({
                "timestamp": row[0],
                "user_message": row[1],
                "agent_response": row[2],
                "tools_used": json.loads(row[3]) if row[3] else []
            })
        
        return list(reversed(conversations))  # Return in chronological order
    
    def add_document(self, file_path: str, summary: Optional[str] = None):
        """Register a document in the database"""
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        
        file_path = Path(file_path)
        
        cursor.execute("""
            INSERT OR REPLACE INTO documents (file_path, file_name, file_type, processed_date, summary)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(file_path),
            file_path.name,
            file_path.suffix,
            datetime.now().isoformat(),
            summary
        ))
        
        conn.commit()
        conn.close()
    
    def save(self):
        """Save FAISS index and metadata to disk"""
        if not VECTOR_AVAILABLE:
            return
        
        try:
            # Save FAISS index
            faiss.write_index(self.index, str(self.vector_store_path / "faiss.index"))
            
            # Save metadata
            with open(self.vector_store_path / "metadata.json", 'w') as f:
                json.dump(self.metadata_store, f)
            
            print("Memory saved successfully")
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def get_context_for_query(self, query: str, max_conversations: int = 3) -> str:
        """
        Get relevant context for a query combining semantic search and recent history
        
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Get semantically similar past interactions
        similar = self.semantic_search(query, k=max_conversations)
        if similar:
            context_parts.append("=== Relevant Past Interactions ===")
            for item in similar:
                if item['type'] == 'conversation':
                    context_parts.append(f"[Similarity: {item['similarity_score']:.2f}]")
                    context_parts.append(f"Time: {item['timestamp']}")
        
        # Get recent conversations for continuity
        recent = self.get_recent_conversations(limit=3)
        if recent:
            context_parts.append("\n=== Recent Conversation History ===")
            for conv in recent[-3:]:  # Last 3
                context_parts.append(f"User: {conv['user_message'][:100]}")
                context_parts.append(f"Agent: {conv['agent_response'][:100]}")
        
        return "\n".join(context_parts) if context_parts else "No relevant context found."


# For testing
if __name__ == "__main__":
    memory = LocalMemorySystem()
    
    # Test adding conversation
    conv_id = memory.add_conversation(
        user_message="What's the weather like?",
        agent_response="I'll search for current weather information.",
        tools_used=["linkup_search"]
    )
    print(f"Added conversation with ID: {conv_id}")
    
    # Test semantic search
    results = memory.semantic_search("weather", k=3)
    print(f"\nSemantic search results: {results}")
    
    # Save
    memory.save()
    print("\nMemory saved!")
