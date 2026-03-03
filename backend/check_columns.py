import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.monday_client import fetch_one_item
import os

async def check():
    deals_board_id = os.getenv("MONDAY_DEALS_BOARD_ID")
    wo_board_id = os.getenv("MONDAY_WORK_ORDERS_BOARD_ID")

    print("=== DEALS BOARD COLUMNS ===")
    item = await fetch_one_item(deals_board_id)
    if item:
        print(f"Item name: {item['name']}")
        for col in item["column_values"]:
            print(f"  ID: {col['id']:<30} | Text: {col['text']}")

    print("\n=== WORK ORDERS BOARD COLUMNS ===")
    item = await fetch_one_item(wo_board_id)
    if item:
        print(f"Item name: {item['name']}")
        for col in item["column_values"]:
            print(f"  ID: {col['id']:<30} | Text: {col['text']}")

asyncio.run(check())