```python
import json
import datetime

class AeroFIXSentinel:
    def __init__(self, max_order_value_usd=1000000, max_quantity_per_trade=10000):
        self.max_order_value_usd = max_order_value_usd
        self.max_quantity_per_trade = max_quantity_per_trade
        print(f"🔒 [SENTINEL INITIALIZED] Risk guardrails active.")
        print(f"   -> Max Single Order Value: ${max_order_value_usd:,}")
        print(f"   -> Max Single Order Qty: {max_quantity_per_trade:,} shares")

    def validate_and_compile_fix(self, agent_payload: dict, simulated_market_price: float) -> dict:
        ticker = agent_payload.get("ticker")
        qty = agent_payload.get("quantity", 0)
        side = agent_payload.get("side") # BUY or SELL
        
        calculated_value = qty * simulated_market_price
        
        print(f"\n⚡ [SENTINEL INBOUND] Evaluating Agent Order: {side.upper()} {qty:,} {ticker}...")

        # Guardrail 1: Volume Check
        if qty > self.max_quantity_per_trade:
            return {"status": "REJECTED", "reason": f"Order quantity {qty:,} exceeds maximum ceiling limit of {self.max_quantity_per_trade:,}."}
            
        # Guardrail 2: Notional Value Check
        if calculated_value > self.max_order_value_usd:
            return {"status": "REJECTED", "reason": f"Total notional value ${calculated_value:,} exceeds risk cap of ${self.max_order_value_usd:,}."}

        # Guardrail 3: Core Compliance/Trading Hours Check (Simulated 9 AM - 5 PM)
        current_hour = datetime.datetime.now().hour
        if current_hour < 9 or current_hour > 17:
            return {"status": "REJECTED", "reason": "Execution blocked: Intended target timestamp falls outside permitted trading window."}

        # If all checks pass, safely compile into valid institutional FIX tag parameters
        fix_message = {
            "Tag_35_MsgType": "D",           # New Order Single
            "Tag_49_SenderCompID": "UNIQUE_GATE_AI",
            "Tag_55_Symbol": ticker,
            "Tag_54_Side": "1" if side.upper() == "BUY" else "2",
            "Tag_38_OrderQty": qty,
            "Tag_44_Price": simulated_market_price,
            "Tag_60_TransactTime": datetime.datetime.utcnow().isoformat()
        }
        
        return {"status": "APPROVED", "fix_payload": fix_message}

if __name__ == "__main__":
    sentinel = AeroFIXSentinel()
    
    # Scenario A: Agent requests a normal, compliant execution
    safe_order = {"ticker": "NVDA", "quantity": 2500, "side": "BUY"}
    result_a = sentinel.validate_and_compile_fix(safe_order, simulated_market_price=120.00)
    print(json.dumps(result_a, indent=2))
    
    # Scenario B: Agent hallucinates or panics and requests an unsafe size
    unsafe_order = {"ticker": "NVDA", "quantity": 50000, "side": "BUY"}
    result_b = sentinel.validate_and_compile_fix(unsafe_order, simulated_market_price=120.00)
    print(json.dumps(result_b, indent=2))
