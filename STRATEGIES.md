# 🚀 Multi-Strategy Algorithmic Allocation Engine

An institutional-grade **Multi-Strategy Portfolio Platform** that simulates a modern Fund-of-Funds (FoF) or pod-shop allocator. The architecture isolates discrete statistical edges across different asset classes and unifies them under a centralized, mathematical risk-parity framework.

```mermaid
graph TD
    Alloc[MultiStratPortfolioAllocator <br> Total Capital: $10.0M]
    
    ELS[EquityLongShort Pod <br> Inverse Vol Weight: 31.6%]
    Macro[GlobalMacro Pod <br> Inverse Vol Weight: 20.9%]
    StatArb[StatArbitrage Pod <br> Inverse Vol Weight: 47.5%]

    Alloc --> ELS
    Alloc --> Macro
    Alloc --> StatArb
