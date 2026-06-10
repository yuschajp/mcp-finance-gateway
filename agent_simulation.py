import asyncio
import json
from register_broker_session import get_unified_research_brief

async def simulate_llm_agent(analyst_prompt: str, target_ticker: str):
    print(f"\n💬 [ANALYST PROMPT]: \"{analyst_prompt} ({target_ticker.upper()})\"")
    print("-" * 70)
    
    print(f"🧠 [LLM REASONING]: Evaluating live risk metrics and narrative sentiment for {target_ticker.upper()}...")
    print("   🚀 ACTION: Requesting live secure context stream via Unique-Gate Gateway...")
    await asyncio.sleep(1) 
    
    # Trigger the live-loading resource link
    raw_gateway_data = await get_unified_research_brief(ticker=target_ticker)
    gateway_data = json.loads(raw_gateway_data)
    
    print("\n🧠 [LLM REASONING]: Data successfully ingested. Compiling final compliance briefing...")
    await asyncio.sleep(0.5)
    
    print("\n🤖 [LLM AGENT RESPONSE]:")
    print("================================================================================")
    print(f"I have compiled the live institutional context for **{gateway_data['asset']}**.")
    print(f"System Link Status: {gateway_data['status']} via {', '.join(gateway_data['sources_compiled'])}\n")
    
    # Print the live, rule-compiled bulleted narrative directly
    print(gateway_data['executive_narrative'])
    
    print(f"\n🛡️  **Proprietary Quant Risk Metrics:**")
    print(f"    • Localized Model Alpha: {gateway_data['internal_quant_signals']['model_alpha']}")
    print(f"    • Daily Value at Risk (VaR 95%): ${gateway_data['internal_quant_signals']['current_var_95']:,}")
    print("================================================================================")
    print("✅ System Status: Secure data link closed. Compliance audit log generated.")

if __name__ == "__main__":
    # Test it with a real ticker like IBM, AAPL, or MSFT
    prompt = "Give me a comprehensive risk update on our exposure including real-time macro sentiment."
    asyncio.run(simulate_llm_agent(prompt, target_ticker="AAPL"))
