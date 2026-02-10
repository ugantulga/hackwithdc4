"""
Main Desktop Intelligence Agent
Integrates Ollama LLM, LangChain, Linkup tools, and local memory
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.tools import BaseTool

# Import our custom tools
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.linkup_tool import create_linkup_tools
from tools.document_tools import create_document_tools
from memory.local_memory import LocalMemorySystem


class DesktopIntelligenceAgent:
    """
    AGI-inspired desktop intelligence agent with:
    - Multi-domain reasoning (documents, web search, memory)
    - Local LLM (Ollama)
    - Privacy-first architecture
    - Contextual memory
    """
    
    def __init__(
        self,
        ollama_model: str = "llama3.2",
        ollama_base_url: str = "http://localhost:11434",
        verbose: bool = True
    ):
        load_dotenv()
        
        self.verbose = verbose
        
        # Initialize local LLM
        print(f"Initializing Ollama with model: {ollama_model}")
        self.llm = Ollama(
            model=ollama_model,
            base_url=ollama_base_url,
            temperature=0.7
        )
        
        # Initialize memory system
        print("Initializing local memory system...")
        self.memory = LocalMemorySystem()
        
        # Initialize tools
        print("Loading tools...")
        self.tools = self._create_tools()
        
        # Create agent
        print("Creating agent...")
        self.agent = self._create_agent()
        
        print(f"✓ Agent initialized with {len(self.tools)} tools")
    
    def _create_tools(self) -> List[BaseTool]:
        """Create all available tools for the agent"""
        tools = []
        
        # Add Linkup web search tools
        try:
            linkup_tools = create_linkup_tools()
            tools.extend(linkup_tools)
            print(f"  ✓ Loaded {len(linkup_tools)} Linkup tools")
        except Exception as e:
            print(f"  ! Warning: Could not load Linkup tools: {e}")
        
        # Add document processing tools
        try:
            doc_tools = create_document_tools()
            tools.extend(doc_tools)
            print(f"  ✓ Loaded {len(doc_tools)} document tools")
        except Exception as e:
            print(f"  ! Warning: Could not load document tools: {e}")
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """Create LangChain ReAct agent"""
        
        # ReAct prompt template
        template = """You are an intelligent desktop assistant with access to tools for web search and document processing. You help users with a wide variety of tasks by reasoning step-by-step and using available tools when needed.

You have access to the following tools:

{tools}

When using tools, follow this format:

Question: the input question or task
Thought: think about what you need to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

IMPORTANT GUIDELINES:
1. Use web search (linkup_search) when you need current information, facts, or verification
2. Use document tools when the user references files or documents
3. Always explain your reasoning in the Thought sections
4. If you're unsure, admit it and use tools to find accurate information
5. Keep responses concise and helpful
6. Respect user privacy - never share local file contents externally

Context from previous interactions:
{context}

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "context"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
        
        # Create ReAct agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            max_iterations=10,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        return agent_executor
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Execute user command with full agent capabilities
        
        Args:
            user_input: User's natural language command
        
        Returns:
            Dict with 'output', 'intermediate_steps', and 'tools_used'
        """
        try:
            # Get relevant context from memory
            context = self.memory.get_context_for_query(user_input)
            
            # Run agent
            result = self.agent.invoke({
                "input": user_input,
                "context": context
            })
            
            # Extract tools used
            tools_used = []
            if "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    if len(step) > 0 and hasattr(step[0], 'tool'):
                        tools_used.append(step[0].tool)
            
            # Store in memory
            self.memory.add_conversation(
                user_message=user_input,
                agent_response=result["output"],
                tools_used=tools_used
            )
            
            # Save memory periodically
            self.memory.save()
            
            return {
                "output": result["output"],
                "intermediate_steps": result.get("intermediate_steps", []),
                "tools_used": tools_used
            }
            
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            print(error_msg)
            
            # Still save to memory for context
            self.memory.add_conversation(
                user_message=user_input,
                agent_response=error_msg,
                tools_used=[]
            )
            
            return {
                "output": error_msg,
                "intermediate_steps": [],
                "tools_used": [],
                "error": str(e)
            }
    
    def chat(self, message: str) -> str:
        """
        Simple chat interface - returns just the response text
        
        Args:
            message: User message
        
        Returns:
            Agent's response as string
        """
        result = self.run(message)
        return result["output"]
    
    def get_tools_info(self) -> str:
        """Get information about available tools"""
        info = "Available Tools:\n\n"
        for tool in self.tools:
            info += f"- {tool.name}:\n  {tool.description}\n\n"
        return info


# For testing
if __name__ == "__main__":
    # Test the agent
    print("="*80)
    print("DESKTOP INTELLIGENCE AGENT TEST")
    print("="*80)
    
    agent = DesktopIntelligenceAgent(verbose=True)
    
    print("\n" + "="*80)
    print("Tools available:")
    print(agent.get_tools_info())
    
    print("\n" + "="*80)
    print("Test 1: Web search")
    print("="*80)
    response = agent.chat("What are the latest developments in quantum computing?")
    print(f"\nAgent Response:\n{response}")
    
    print("\n" + "="*80)
    print("Test 2: Follow-up (memory test)")
    print("="*80)
    response = agent.chat("Can you tell me more about that?")
    print(f"\nAgent Response:\n{response}")
