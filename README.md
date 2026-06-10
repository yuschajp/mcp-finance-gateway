# MCP Finance Gateway (`Unique-Gate`)

[![MCP Gateway Integration Test](https://github.com/yuschajp/mcp-finance-gateway/actions/workflows/mcp-test.yml/badge.svg)](https://github.com/yuschajp/mcp-finance-gateway/actions)

An institutional-grade implementation of the **Model Context Protocol (MCP)** designed for multi-broker session isolation, secure authentication mapping via OIDC layout, and real-time portfolio resource streaming.

This gateway bridges the gap between agentic LLM context windows and secure capital markets data endpoints, bypassing traditional end-of-day batch processing lag and manual single sign-on (SSO) barriers.

---

## 🏗️ Architecture Overview

### System Workflow Blueprint

```mermaid
graph TD
    classDef analyst fill:#e6f7ff,stroke:#1890ff,stroke-width:2px;
    classDef agent fill:#f9f0ff,stroke:#722ed1,stroke-width:2px;
    classDef gateway fill:#fff7e6,stroke:#ffa940,stroke-width:2px;
    classDef secure fill:#f6ffed,stroke:#52c41a,stroke-width:2px;

    Analyst[🕵️‍♂️ Front-Office Analyst]:::analyst
    Agent[🧠 LLM Risk Agent]:::agent
    Gateway[🔐 Unique-Gate Gateway]:::gateway
    
    subgraph Upstream Intelligence (Context)
        SSO[Bank Feed via SSO]:::secure
        S3[Alternative Data S3]:::secure
        Quant[On-Prem Risk Models]:::secure
    end

    subgraph Downstream Execution (Safety)
        FIX[AeroFIX Sentinel Firewall]:::gateway
        Venue[Execution Venue / Broker]:::secure
    end

    Analyst -->|1. Prompt Portfolio Request| Agent
    Agent -->|2. Request URI: research://| Gateway
    
    Gateway -->|3. Background SSO & Token Exchange| Upstream Intelligence
    Upstream Intelligence -->|4. Standardized Context Stream| Gateway
    Gateway -->|5. Deliver Clean JSON Block| Agent
    
    Agent -->|6. Propose Execution Intent| FIX
    FIX -->|7. Hard Risk Cap Validation| Venue
```

The gateway operates across two primary vector spaces to handle sensitive institutional workflows:

*   **Downstream Operations (Session Isolation Tool):** Dynamically instantiates isolated runtime environments for unique brokerage integrations mapped via secure token parameters to prevent horizontal data leaks.
*   **Upstream Intelligence (Cross-Source Research Stream):** Normalizes fragmented research endpoints—whether they are behind an external vendor's SSO or an internal secure cloud database—into standardized URI schemes (`research://`).

---

## 💻 Agentic Cognitive Loop Simulation

The repository includes an end-to-end client-side simulation (`agent_simulation.py`) that demonstrates how an LLM agent uses the protocol to orchestrate data aggregation automatically when asked a complex question by an analyst.

### How it Works:
1. **The Request:** An analyst prompts the agent for a unified risk assessment on an equity exposure (e.g., `NVDA`).
2. **The Interception:** The agent identifies that the required insights are trapped across multiple administrative silos (Premium Portal SSO, AWS S3 buckets, and local on-premise risk clusters).
3. **The Resolve:** The agent requests a secure context stream via the gateway URI (`research://NVDA/unified-brief`), bypassing data walls and returning a compliant JSON block.

### To Run the Simulation Locally:
```bash
pip install "mcp[cli]"
python agent_simulation.py
