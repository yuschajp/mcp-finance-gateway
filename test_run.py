from register_broker_session import register_broker_session, get_broker_positions
import asyncio

async def main():
    print("⚡ STEP 1: Executing Session Isolation Tool...")
    # Register the session
    auth_result = await register_broker_session(
        broker_id="Goldman_Sachs",
        client_id="inst_client_01",
        zitadel_token="Bearer token_12345",
        api_endpoint="https://api.gs.com"
    )
    print(f"Response: {auth_result}\n")

    print("🛰️ STEP 2: AI Agent requesting data stream via resource URI ('broker://Goldman_Sachs/positions')...")
    # Pull the live resource data from the isolated workspace
    data_stream = await get_broker_positions(broker_id="Goldman_Sachs")
    print("Active Workspace Data Output:")
    print(data_stream)

asyncio.run(main())
