import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from database import create_document
from schemas import TradeAccount, QuoteRequest

app = FastAPI(title="Verdure Mulch Glue API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeadResponse(BaseModel):
    id: str
    status: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Verdure Mulch Glue API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
        response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
        response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Lead capture: trade account
@app.post("/api/trade-account", response_model=LeadResponse)
async def create_trade_account(lead: TradeAccount):
    try:
        insert_id = create_document("tradeaccount", lead)
        return LeadResponse(id=insert_id, status="ok", message="Trade account request received")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lead capture: quote request
@app.post("/api/quote", response_model=LeadResponse)
async def create_quote(req: QuoteRequest):
    try:
        insert_id = create_document("quoterequest", req)
        return LeadResponse(id=insert_id, status="ok", message="Quote request received")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple email auto-response simulation endpoint (in real world, integrate provider)
class ContactEmail(BaseModel):
    to: EmailStr
    subject: str
    body: str

@app.post("/api/email/auto-reply")
async def email_auto_reply(payload: ContactEmail):
    # In this environment, we'll just acknowledge the request
    return {"status": "queued", "to": payload.to}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
