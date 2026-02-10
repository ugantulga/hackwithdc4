# Project Overview

This project is an email assistant meant to assist you in responding to business emails. This assistant also uses [Linkup](https://app.linkup.so/home) to search the web for additional information about the people, companies, situations in the email, and uses that information to help you craft a response. 

## Tech Stack 

 ### Models used
- Deepseek
### APIs used
- Linkup

## Workflow
1. Agent connects to inbox and reads emails
2. Emails are classified into pre-determined categories: spam, personal, work & all non-work emails are ignored
3. Based on the user prompt, the Agent selects a work email, summarizes it, and displays the summary to the user, highlighting key details such as sender name, company, request, ect…
4. The agent asks the user if they want any of the data (person, company, etc…) enriched using Linkup.
    a). If user says no, the process ends
   b). If user says yes, the agent connects to Linkup and passes along the required info
6. Linkup runs a web search to enrich data and passes the information back to the agent
7. The agent verifies the Linkup information using external sources (ex. Crunchbase, Bloomberg, LinkedIn, ect.) 
8. The agent summarizes the information for the user and asks if the user wants a drafted reply
   a). If user says no, the process ends
   b). If user says yes, the agent drafts a reply based on email context and the enriched data

## Architecture 

### System Design Diagram 
<img width="466" height="886" alt="SD" src="https://github.com/user-attachments/assets/deaf91b9-b1ba-4623-94f9-8ab85b0dad39" />

### Data Flow
```
Gmail Inbox ──▶ readEmail.py ──▶ EmailConductor.py ──▶  DeepSeek LLM
                     │                   │
                     │                   ├─ classify_email()
                     │                   ├─ summarize_email()
                     │                   └─ draft_reply_email()
                     │                   │
                     └───────── EmailRecord (dataclass) ◀──┘

  ```
| Module | Purpose |
|---|---|
| **`EmailRecord.py`** | Dataclass holding email fields: `id`, `subject`, `body`, `category`, `action`, `summary`, `draft_reply` |
| **`EmailConductor.py`** | LLM chains for classification, summarization, and reply drafting; action routing logic |
| **`readEmail.py`** | Connects to Gmail via IMAP, extracts subject/body, and sends each email through the pipeline |

## Category → Action Mapping

| Category | Action |
|---|---|
| Spam / Scam | 🗑️ Delete / Ignore |
| Friends / Personal | 📝 Summarize + Draft Reply |
| Delivery | 📦 Summarize |
| Scheduling | 📅 Summarize + Draft Reply |
| Other | 🔍 Review Manually |

## Setup 

### Requirements

### Installation


## Current Challenges and Future Plans

### Challenges

One current challenge we have is trustworthiness of information. We need an AI agent to verify that the information pulled from the web search is correct.

### Future Plans

In the future the assistant should be able to pull from multiple sources such as an internal knowlege repository in addition to the web search. 

We also plan to rotate AI models to determine which is the best model to use for which task. Ex. Claude for interfacing with the Linkup API and Ollama for talking to the user. 

