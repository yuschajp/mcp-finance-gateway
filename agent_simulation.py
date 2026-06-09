import asyncio
import json
from register_broker_session import get_unified_research_brief

async def simulate_llm_agent(analyst_prompt: str):
    print(f"\n💬 [ANALYST PROMPT]: \"{analyst_prompt}\"")
    print("-" * 60)
    
    # Step 1: Cognitive Loop - Agent detects missing context
    print("🧠 [LLM REASONING]: I need to evaluate the risk and macro outlook for NVDA.")
    print("   ⚠️  CRITICAL: Data is fragmented across Premium SSO portals, AWS S3, and the Internal Quant Desk.")
    print("   🚀 ACTION: Requesting secure unified context stream from MCP Finance Gateway...")
    await asyncio.sleep(1) # Simulating slight processing pause
    
    # Step 2: Agent requests the resource URI from the gateway
    raw_gateway_data = await get_unified_research_brief(ticker="NVDA")
    gateway_data = json.loads(raw_gateway_data)
    
    # Step 3: Cognitive Loop - Agent digests the secure data and formats a response
    print("\n🧠 [LLM REASONING]: Unified secure data ingested successfully. Analyzing risk parameters...")
    await asyncio.sleep(1)
    
    print("\n🤖 [LLM AGENT RESPONSE]:")
    print("================================================================================")
    print(f"I have compiled the institutional context for **{gateway_data['asset']}** by securely")
    print(f"bypassing administrative silos across {', '.join(gateway_data['sources_compiled'])}.\n")
    
    print(f"📈  **Macro Research Summary:**\n    {gateway_data['macro_research']['insight']}\n")
    
    print(f"📊  **Alternative Data Streams:**")
    print(f"    • Consumer Spending: {gateway_data['alternative_metrics']['consumer_spend_trend']}")
    print(f"    • Supply Chain Delays: {gateway_data['alternative_metrics']['supply_chain_delay_days']} days\n")
    
    print(f"🛡️  **Proprietary Quant Risk Metrics:**")
    print(f"    • Localized Model Alpha: {gateway_data['internal_quant_signals']['model_alpha']}")
    print(f"    • Daily Value at Risk (VaR 95%): ${gateway_data['internal_quant_signals']['current_var_95']:,}")
    print("================================================================================")
    print("✅ System Status: Secure data link closed. Compliance audit log generated.")

if __name__ == "__main__":
    # Test prompt from an institutional analyst
    prompt = "Give me a comprehensive risk update on our NVDA exposure including macro sentiment and alternative data."
    asyncio.run(simulate_llm_agent(prompt))
