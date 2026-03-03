# Monday.com BI Agent

An AI-powered business intelligence chatbot that answers founder-level queries 
using live Monday.com data.

## Tech Stack
- Frontend: React + TypeScript + Vite
- Backend: Python + FastAPI
- LLM: Groq (llama-3.3-70b-versatile)
- Data Source: Monday.com GraphQL API

## Project Structure
```
monday-bi-agent/
├── backend/
│   ├── tools/
│   │   ├── monday_client.py
│   │   └── normalizer.py
│   ├── main.py
│   ├── agent.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       └── App.tsx
└── README.md
```

## Running Locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with:
# GROQ_API_KEY=your_key
# MONDAY_API_TOKEN=your_token
# MONDAY_DEALS_BOARD_ID=your_id
# MONDAY_WORK_ORDERS_BOARD_ID=your_id

uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

| Variable | Description |
|---|---|
| GROQ_API_KEY | Groq API key |
| MONDAY_API_TOKEN | Monday.com API token |
| MONDAY_DEALS_BOARD_ID | Deals board ID |
| MONDAY_WORK_ORDERS_BOARD_ID | Work Orders board ID |
| VITE_API_URL | Backend URL (for frontend) |

## Monday.com Boards
- Deals Board: [paste your Monday.com share link here]
- Work Orders Board: [paste your Monday.com share link here]
