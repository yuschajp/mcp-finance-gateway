# MCP Finance Gateway (`Unique-Gate`)

An institutional-grade implementation of the **Model Context Protocol (MCP)** designed for multi-broker session isolation, secure authentication mapping via OIDC layout, and real-time portfolio resource streaming.

## 🏗️ Architecture Overview
This framework bridges the gap between agentic LLM context windows and secure capital markets data endpoints, bypassing traditional end-of-day batch processing lag.

1. **Session Isolation (Tool):** Dynamically instantiates isolated runtime environments for unique brokerage integrations mapped via secure token parameters.
2. **Context Streaming (Resource):** Exposes read-only, schema-enforced URI pathways (`broker://{broker_id}/positions`) enabling AI risk agents to safely pull live position data and systemic risk metrics (`DV01`) without horizontal data exposure.

## 🛠️ Components
* `register_broker_session.py`: Core asynchronous FastMCP server engine.
* `test_run.py`: End-to-end integration test simulating the tool-to-resource data loop.

## 💻 Quick Start
```bash
pip install "mcp[cli]"
python test_run.py
\`\`\`
