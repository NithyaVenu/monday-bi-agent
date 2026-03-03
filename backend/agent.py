# from openai import OpenAI
# from tools.monday_client import fetch_deals, fetch_work_orders
# from tools.normalizer import normalize_items
# import json
# import os

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "fetch_deals",
#             "description": "Fetch all deals data from Monday.com. Use for questions about pipeline, revenue, sales, clients, deal stages.",
#             "parameters": {"type": "object", "properties": {}, "required": []}
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "fetch_work_orders",
#             "description": "Fetch all work orders from Monday.com. Use for questions about projects, work status, deliverables, operations.",
#             "parameters": {"type": "object", "properties": {}, "required": []}
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "fetch_both",
#             "description": "Fetch both deals and work orders. Use when the question spans across pipeline and operations.",
#             "parameters": {"type": "object", "properties": {}, "required": []}
#         }
#     }
# ]

# async def run_agent(user_message: str, history: list[dict]) -> dict:
#     trace = []
#     messages = [
#         {
#             "role": "system",
#             "content": """You are a business intelligence assistant for a founder. 
#             You have access to Monday.com boards containing Deals and Work Orders data.
#             Always fetch live data before answering. Be concise, insight-driven, and always 
#             mention data quality caveats at the end of your response if data was messy or incomplete."""
#         },
#         *history,
#         {"role": "user", "content": user_message}
#     ]

#     # First LLM call — let it decide which tools to call
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=messages,
#         tools=tools,
#         tool_choice="auto"
#     )

#     message = response.choices[0].message

#     # If the LLM wants to call tools
#     if message.tool_calls:
#         messages.append(message)

#         for tool_call in message.tool_calls:
#             fn_name = tool_call.function.name
#             trace.append({"tool": fn_name, "status": "calling..."})

#             if fn_name == "fetch_deals":
#                 raw = await fetch_deals()
#                 data, caveats = normalize_items(raw)
#                 result = {"deals": data, "caveats": caveats}

#             elif fn_name == "fetch_work_orders":
#                 raw = await fetch_work_orders()
#                 data, caveats = normalize_items(raw)
#                 result = {"work_orders": data, "caveats": caveats}

#             elif fn_name == "fetch_both":
#                 raw_deals = await fetch_deals()
#                 raw_wo = await fetch_work_orders()
#                 deals, c1 = normalize_items(raw_deals)
#                 wos, c2 = normalize_items(raw_wo)
#                 result = {"deals": deals, "work_orders": wos, "caveats": c1 + c2}

#             trace[-1]["status"] = "done"
#             trace[-1]["records_returned"] = len(result.get("deals", result.get("work_orders", [])))

#             messages.append({
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "content": json.dumps(result)
#             })

#         # Second LLM call — generate the final answer with data
#         final_response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=messages
#         )
#         answer = final_response.choices[0].message.content

#     else:
#         # LLM answered directly (e.g. clarifying question)
#         answer = message.content

#     return {"answer": answer, "trace": trace}

from groq import Groq
from tools.monday_client import fetch_deals, fetch_work_orders
from tools.normalizer import normalize_items
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def summarize_data(result: dict, max_records: int = 20) -> dict:
#     """Trim data to avoid token limits while keeping key info"""
#     summarized = {}

#     if "deals" in result:
#         deals = result["deals"]
#         summarized["deals_total_count"] = len(deals)
#         summarized["deals_sample"] = deals[:max_records]  # only first 20
#         summarized["caveats"] = result.get("caveats", [])[:10]  # limit caveats too

#     if "work_orders" in result:
#         wos = result["work_orders"]
#         summarized["work_orders_total_count"] = len(wos)
#         summarized["work_orders_sample"] = wos[:max_records]
#         if "caveats" not in summarized:
#             summarized["caveats"] = result.get("caveats", [])[:10]

#     if "error" in result:
#         summarized["error"] = result["error"]

#     return summarized
def summarize_data(result: dict, max_records: int = 20) -> dict:
    """Trim data to avoid token limits while keeping key info"""
    summarized = {}

    if "deals" in result:
        deals = result["deals"]
        summarized["deals_total_count"] = len(deals)

        # For cross-board queries, only keep key fields instead of full records
        summarized["deals_sample"] = [
            {
                "name": d.get("name"),
                "company": d.get("company"),
                "sector": d.get("sector"),
                "deal_value": d.get("deal_value"),
                "deal_stage": d.get("deal_stage"),
                "status": d.get("status"),
                "expected_close_date": d.get("expected_close_date")
            }
            for d in deals[:10]  # only 10 for cross-board
        ]

    if "work_orders" in result:
        wos = result["work_orders"]
        summarized["work_orders_total_count"] = len(wos)

        # Only keep key fields
        summarized["work_orders_sample"] = [
            {
                "name": w.get("name"),
                "company": w.get("company"),
                "sector": w.get("sector"),
                "status": w.get("status"),
                "contract_value": w.get("contract_value"),
                "linked_deal": w.get("linked_deal"),
                "start_date": w.get("start_date"),
                "end_date": w.get("end_date")
            }
            for w in wos[:10]  # only 10 for cross-board
        ]

    # Only include caveats that mention important fields, limit to 5
    if "caveats" in result:
        important_keywords = ["sector", "company", "deal_value", "contract_value", "status"]
        filtered_caveats = [
            c for c in result["caveats"]
            if any(k in c for k in important_keywords)
        ]
        summarized["caveats"] = filtered_caveats[:5]

    if "error" in result:
        summarized["error"] = result["error"]

    return summarized

async def run_agent(user_message: str, history: list[dict]) -> dict:
    trace = []

    # Format conversation history for context
    history_text = ""
    if history:
        for msg in history[-4:]:  # only last 4 messages to save tokens
            role = "User" if msg.get("role") == "user" else "Assistant"
            history_text += f"{role}: {msg.get('content', '')}\n"

    # First Groq call — decide which tool to call
    tool_decision = client.chat.completions.create(
        # model="llama-3.3-70b-versatile",
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a tool selector for a business intelligence assistant.
                Based on the user's question, reply with ONLY one of these exact strings, nothing else:
                - fetch_deals        (pipeline, revenue, sales, clients, deal stage questions)
                - fetch_work_orders  (projects, work status, deliverables, operations questions)
                - fetch_both         (questions spanning both pipeline and operations)
                - none               (greetings or questions needing no data)"""
            },
            {
                "role": "user",
                "content": f"Previous conversation:\n{history_text if history_text else 'None'}\n\nCurrent question: {user_message}"
            }
        ],
        temperature=0
    )

    tool_choice = tool_decision.choices[0].message.content.strip().lower()
    result = {}

    # Execute the chosen tool
    if "fetch_both" in tool_choice:
        trace.append({"tool": "fetch_both", "status": "calling..."})
        try:
            raw_deals = await fetch_deals()
            raw_wo = await fetch_work_orders()
            deals, c1 = normalize_items(raw_deals, board_type="deals")
            wos, c2 = normalize_items(raw_wo, board_type="work_orders")
            result = {"deals": deals, "work_orders": wos, "caveats": c1 + c2}
            trace[-1]["status"] = "done"
            trace[-1]["records_returned"] = len(deals) + len(wos)
        except Exception as e:
            trace[-1]["status"] = f"error: {str(e)}"
            result = {"error": str(e)}

    elif "fetch_deals" in tool_choice:
        trace.append({"tool": "fetch_deals", "status": "calling..."})
        try:
            raw = await fetch_deals()
            data, caveats = normalize_items(raw, board_type="deals")
            result = {"deals": data, "caveats": caveats}
            trace[-1]["status"] = "done"
            trace[-1]["records_returned"] = len(data)
        except Exception as e:
            trace[-1]["status"] = f"error: {str(e)}"
            result = {"error": str(e)}

    elif "fetch_work_orders" in tool_choice:
        trace.append({"tool": "fetch_work_orders", "status": "calling..."})
        try:
            raw = await fetch_work_orders()
            data, caveats = normalize_items(raw, board_type="work_orders")
            result = {"work_orders": data, "caveats": caveats}
            trace[-1]["status"] = "done"
            trace[-1]["records_returned"] = len(data)
        except Exception as e:
            trace[-1]["status"] = f"error: {str(e)}"
            result = {"error": str(e)}

    else:
        trace.append({"tool": "none", "status": "no API call needed"})

    # Trim data before sending to LLM to avoid token limits
    trimmed_result = summarize_data(result)

#     # Second Groq call — generate the final BI answer
#     final_response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """You are a business intelligence assistant for a founder.
#                 Be concise, insight-driven, and always mention data quality caveats
#                 if data was messy or incomplete. Use specific numbers where available.
#                 Note: You may be seeing a sample of the full dataset — total counts are provided.
#                 End every data-driven response with a short 📋 Data Notes section covering:
#                 - Total records in board vs records analyzed
#                 - Any missing fields or normalizations applied
#                 - Any caveats the founder should know"""
#             },
#             {
#                 "role": "user",
#                 "content": f"""Previous conversation:
# {history_text if history_text else "None"}

# Current question: {user_message}

# Live data from Monday.com (sample of full dataset):
# {json.dumps(trimmed_result, indent=2) if trimmed_result else "No data fetched for this query."}"""
#             }
#         ],
#         temperature=0.3,
#         max_tokens=1024
#     )
# Detect if this is a cross-board query
    is_cross_board = "deals" in trimmed_result and "work_orders" in trimmed_result

    final_response = client.chat.completions.create(
        # model="llama-3.3-70b-versatile",
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a business intelligence assistant for a founder.
                Be concise and insight-driven. Use specific numbers where available.
                Keep your response under 300 words.
                End with a short 📋 Data Notes section (2-3 lines max) covering:
                - Total records in each board vs records analyzed
                - Any key caveats"""
            },
            {
                "role": "user",
                "content": f"""Previous conversation:
{history_text if history_text else "None"}

Current question: {user_message}

Live data from Monday.com:
{json.dumps(trimmed_result, indent=2) if trimmed_result else "No data fetched."}"""
            }
        ],
        temperature=0.3,
        max_tokens=512 if is_cross_board else 1024
    )

    answer = final_response.choices[0].message.content

    return {"answer": answer, "trace": trace}