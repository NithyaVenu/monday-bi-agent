# import httpx
# import os
# from dotenv import load_dotenv

# load_dotenv()

# MONDAY_API_URL = "https://api.monday.com/v2"
# MONDAY_API_TOKEN = os.getenv("MONDAY_API_TOKEN")
# DEALS_BOARD_ID = os.getenv("MONDAY_DEALS_BOARD_ID")
# WORK_ORDERS_BOARD_ID = os.getenv("MONDAY_WORK_ORDERS_BOARD_ID")

# headers = {
#     "Authorization": MONDAY_API_TOKEN,
#     "Content-Type": "application/json"
# }

# async def fetch_board(board_id: str) -> list[dict]:
#     query = """
#     query ($boardId: [ID!]) {
#       boards(ids: $boardId) {
#         items_page(limit: 500) {
#           items {
#             id
#             name
#             column_values {
#               id
#               text
#               value
#             }
#           }
#         }
#       }
#     }
#     """
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             MONDAY_API_URL,
#             json={"query": query, "variables": {"boardId": [board_id]}},
#             headers=headers,
#             timeout=30.0
#         )

#         # Print raw response so you can see exactly what Monday.com returns
#         raw = response.json()
#         print("Monday.com raw response:", raw)

#         # Check for API errors
#         if "errors" in raw:
#             raise Exception(f"Monday.com API error: {raw['errors']}")

#         # Check response structure step by step
#         if "data" not in raw:
#             raise Exception(f"No 'data' in response: {raw}")

#         if "boards" not in raw["data"]:
#             raise Exception(f"No 'boards' in response data: {raw['data']}")

#         boards = raw["data"]["boards"]

#         if not boards or len(boards) == 0:
#             raise Exception(f"No boards found for board_id {board_id}. Check your board ID in .env")

#         items = boards[0].get("items_page", {}).get("items", [])
#         print(f"Fetched {len(items)} items from board {board_id}")
#         return items

# async def fetch_deals():
#     print(f"Fetching deals from board ID: {DEALS_BOARD_ID}")
#     return await fetch_board(DEALS_BOARD_ID)

# async def fetch_work_orders():
#     print(f"Fetching work orders from board ID: {WORK_ORDERS_BOARD_ID}")
#     return await fetch_board(WORK_ORDERS_BOARD_ID)

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_API_TOKEN = os.getenv("MONDAY_API_TOKEN")
DEALS_BOARD_ID = os.getenv("MONDAY_DEALS_BOARD_ID")
WORK_ORDERS_BOARD_ID = os.getenv("MONDAY_WORK_ORDERS_BOARD_ID")

headers = {
    "Authorization": MONDAY_API_TOKEN,
    "Content-Type": "application/json",
    "API-Version": "2024-01"
}

async def fetch_board(board_id: str) -> list[dict]:
    query = """
    query ($boardId: [ID!]) {
      boards(ids: $boardId) {
        items_page(limit: 500) {
          items {
            id
            name
            column_values {
              id
              text
              value
            }
          }
        }
      }
    }
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            MONDAY_API_URL,
            json={"query": query, "variables": {"boardId": [board_id]}},
            headers=headers,
            timeout=30.0
        )

        raw = response.json()
        print("Monday.com raw response:", raw)

        if "errors" in raw:
            raise Exception(f"Monday.com API error: {raw['errors']}")

        if "data" not in raw:
            raise Exception(f"No 'data' in response: {raw}")

        if "boards" not in raw["data"]:
            raise Exception(f"No 'boards' in response data: {raw['data']}")

        boards = raw["data"]["boards"]

        if not boards or len(boards) == 0:
            raise Exception(f"No boards found for board_id {board_id}. Check your board ID in .env")

        items = boards[0].get("items_page", {}).get("items", [])
        print(f"Fetched {len(items)} items from board {board_id}")
        return items

async def fetch_one_item(board_id: str) -> dict:
    query = """
    query ($boardId: [ID!]) {
      boards(ids: $boardId) {
        items_page(limit: 1) {
          items {
            id
            name
            column_values {
              id
              text
              value
            }
          }
        }
      }
    }
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            MONDAY_API_URL,
            json={"query": query, "variables": {"boardId": [board_id]}},
            headers=headers,
            timeout=30.0
        )

        raw = response.json()

        if "errors" in raw:
            raise Exception(f"Monday.com API error: {raw['errors']}")

        if "data" not in raw:
            raise Exception(f"No 'data' in response: {raw}")

        boards = raw["data"]["boards"]

        if not boards or len(boards) == 0:
            raise Exception(f"No boards found for board_id {board_id}")

        items = boards[0].get("items_page", {}).get("items", [])
        return items[0] if items else {}

async def fetch_deals():
    print(f"Fetching deals from board ID: {DEALS_BOARD_ID}")
    return await fetch_board(DEALS_BOARD_ID)

async def fetch_work_orders():
    print(f"Fetching work orders from board ID: {WORK_ORDERS_BOARD_ID}")
    return await fetch_board(WORK_ORDERS_BOARD_ID)