# AI Personality Switchboard

A FastAPI + LangChain project that:
- Rewrites text in different AI personas
- Generates multi-persona responses
- Runs AI debates between personas
- Maintains session-based memory using debate_id

## Run Locally

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env:
OPENAI_API_KEY=your_key_here

Start server:
python -m uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs
