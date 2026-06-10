import curses
import time
import json
import asyncio
from register_broker_session import get_unified_research_brief
from aerofix_sentinel import AeroFIXSentinel

async def run_dashboard(stdscr):
    # Hide cursor and set non-blocking input
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    
    # Initialize Color Pairs
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Headers
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Approvals / High Alpha
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Rejections
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Alerts
    
    # Instantiate your actual FIX sentinel firewall
    sentinel = AeroFIXSentinel()
    
    # Simulated orders streaming into the firewall
    order_stream = [
        {"ticker": "AAPL", "quantity": 1500, "side": "BUY", "price": 185.00},
        {"ticker": "NVDA", "quantity": 45000, "side": "BUY", "price": 120.00}, # Will reject
        {"ticker": "MSFT", "quantity": 3000, "side": "SELL", "price": 420.00},
        {"ticker": "AAPL", "quantity": 12000, "side": "BUY", "price": 185.00}, # Will reject
        {"ticker": "NVDA", "quantity": 8000, "side": "BUY", "price": 120.00}
    ]
    
    audit_logs = ["[SYSTEM] Unique-Gate Monitor active. Press 'q' to exit."]
    current_order_idx = 0
    last_update_time = 0
    ticker_list = ["AAPL", "MSFT", "NVDA"]
    current_ticker_idx = 0
    
    # Load initial news cache container
    raw_brief = await get_unified_research_brief(ticker_list[current_ticker_idx])
    brief_data = json.loads(raw_brief)
    
    while True:
        # Clear screen base
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        
        # Guard minimum terminal size
        if width < 80 or height < 22:
            stdscr.addstr(0, 0, "Terminal window too small! Stretch it wider.")
            stdscr.refresh()
            await asyncio.sleep(0.5)
            continue

        current_time = time.time()
        
        # Every 7 seconds, rotate tickers, fetch fresh intel, and process an inbound order intent
        if current_time - last_update_time > 7.0:
            last_update_time = current_time
            
            # 1. Rotate & Live-Load Upstream Data Feed
            current_ticker_idx = (current_ticker_idx + 1) % len(ticker_list)
            target_ticker = ticker_list[current_ticker_idx]
            raw_brief = await get_unified_research_brief(target_ticker)
            brief_data = json.loads(raw_brief)
            
            # 2. Process Next Downstream Order Through AeroFIX Firewall
            order = order_stream[current_order_idx]
            current_order_idx = (current_order_idx + 1) % len(order_stream)
            
            timestamp = time.strftime("%H:%M:%S")
            audit_logs.append(f"[{timestamp}] [INBOUND] Agent intent: {order['side']} {order['quantity']:,} {order['ticker']}")
            
            # Run transaction through your validation logic
            res = sentinel.validate_and_compile_fix(order, order["price"])
            
            if res["status"] == "APPROVED":
                audit_logs.append(f"[{timestamp}] [APPROVED] FIX Msg compiled: Tag_35=D | Tag_38={order['quantity']}")
            else:
                audit_logs.append(f"[{timestamp}] [REJECTED] FIREWALL BLOCK: {res['reason']}")

        # --- DRAW VISUAL INTERFACE PANELS ---
        # Draw Main Banner border
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.border() # Draw large outmost layout frame
        stdscr.addstr(1, 2, " 🔐 UNIQUE-GATE  |  REAL-TIME RISK COMPLIANCE & PROTOCOL GATEWAY ENGINE ")
        stdscr.addstr(2, 1, "-" * (width - 2))
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        # Draw Upstream Title Section
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(4, 2, " 📰 UPSTREAM CONTEXT EXTRACTION STREAM (LIVE FED SENTIMENT) ")
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        # Cleanly slice out and display the compiled narrative text bullets
        narrative_lines = brief_data.get("executive_narrative", "").split("\n\n")
        line_y = 6
        for line in narrative_lines[:3]:
            clean_line = line.replace("• ", "").replace("**", "").replace("_", "")
            split_width = int(width * 0.50)
            if len(clean_line) > split_width:
                clean_line = clean_line[:split_width - 3] + "..."
            stdscr.addstr(line_y, 2, f"• {clean_line}")
            line_y += 2

        # Draw Vertical Panel Divider line mid-way on screen
        for y in range(4, 13):
            stdscr.addstr(y, int(width * 0.53), "|")

        # Draw Downstream Quant Ledger Title Section (Right Side)
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(4, int(width * 0.55), " 🛡️  QUANTITATIVE RISK CONSTRAINT LEDGER ")
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        stdscr.addstr(6, int(width * 0.55), f"Target Exposure:  {brief_data.get('asset', 'N/A')}")
        stdscr.addstr(8, int(width * 0.55), f"Data Link Status: {brief_data.get('status', 'N/A')}")
        
        stdscr.addstr(10, int(width * 0.55), "Localized Alpha:  ")
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr("0.042 (4.20%)")
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
        
        stdscr.addstr(12, int(width * 0.55), "Daily VaR (95%):  ")
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr("$145,000 / $1.0M Cap")
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

        # Draw Horizontal Divider above audit logs
        stdscr.addstr(14, 1, "-" * (width - 2))
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(14, 2, " 🔒 DOWNSTREAM AEROFIX SENTINEL AUDIT TRAIL (DETERMINISTIC COMPLIANCE) ")
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        log_y = 16
        max_logs_to_show = height - 19
        for log in audit_logs[-max_logs_to_show:]:
            if "APPROVED" in log:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(log_y, 2, log[:width-4])
                stdscr.attroff(curses.color_pair(2))
            elif "REJECTED" in log or "FIREWALL BLOCK" in log:
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(log_y, 2, log[:width-4])
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(log_y, 2, log[:width-4])
            log_y += 1
            
        stdscr.refresh()
        
        try:
            key = stdscr.getkey()
            if key == 'q' or key == 'Q':
                break
        except Exception:
            pass
            
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(curses.wrapper(run_dashboard))
