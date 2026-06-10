# MCP Finance Gateway (`Unique-Gate`)

[![MCP Gateway Integration Test](https://github.com/yuschajp/mcp-finance-gateway/actions/workflows/mcp-test.yml/badge.svg)](https://github.com/yuschajp/mcp-finance-gateway/actions)

An institutional-grade implementation of the **Model Context Protocol (MCP)** designed for multi-broker session isolation, secure authentication mapping via OIDC layout, and real-time portfolio resource streaming.

This gateway bridges the gap between agentic LLM context windows and secure capital markets data endpoints, bypassing traditional end-of-day batch processing lag and manual single sign-on (SSO) barriers.

---

## 🏗️ Architecture Overview

The gateway operates across two primary vector spaces to handle sensitive institutional workflows:

* **Upstream Intelligence (Context Aggregation):** Normalizes fragmented research endpoints—whether behind an external vendor's SSO or an internal secure cloud database—into standardized, read-only URI schemes (`research://`).
* **Downstream Operations (Session Isolation & Safety):** Dynamically instantiates isolated runtime environments for unique brokerage integrations mapped via secure token parameters to prevent horizontal data leaks, while enforcing deterministic risk firewalls.

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
    
    subgraph Upstream["Upstream Intelligence (Context)"]
        SSO[Bank Feed via SSO]:::secure
        S3[Alternative Data S3]:::secure
        Quant[On-Prem Risk Models]:::secure
    end

    subgraph Downstream["Downstream Execution (Safety)"]
        FIX[AeroFIX Sentinel Firewall]:::gateway
        Venue[Execution Venue / Broker]:::secure
    end

    Analyst -->|1. Prompt Portfolio Request| Agent
    Agent -->|2. Request URI: research://| Gateway
    
    Gateway -->|3. Background SSO & Token Exchange| Upstream
    Upstream -->|4. Standardized Context Stream| Gateway
    Gateway -->|5. Deliver Clean JSON Block| Agent
    
    Agent -->|6. Propose Execution Intent| FIX
    FIX -->|7. Hard Risk Cap Validation| Venue
