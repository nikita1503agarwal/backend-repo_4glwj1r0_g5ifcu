import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Property, Inquiry

app = FastAPI(title="Team Jafri Realty API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Team Jafri Realty API running"}

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
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Helpers
class IdResponse(BaseModel):
    id: str

# Properties endpoints
@app.post("/api/properties", response_model=IdResponse)
async def create_property(prop: Property):
    try:
        inserted_id = create_document("property", prop)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/properties")
async def list_properties(city: Optional[str] = None, status: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {}
        if city:
            filter_dict["city"] = city
        if status:
            filter_dict["status"] = status
        docs = get_documents("property", filter_dict, limit)
        # serialize ObjectId and datetime
        for d in docs:
            d["id"] = str(d.pop("_id"))
            for k, v in list(d.items()):
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/properties/{prop_id}")
async def get_property(prop_id: str):
    try:
        doc = db["property"].find_one({"_id": ObjectId(prop_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Property not found")
        doc["id"] = str(doc.pop("_id"))
        for k, v in list(doc.items()):
            if hasattr(v, "isoformat"):
                doc[k] = v.isoformat()
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Inquiries endpoints
@app.post("/api/inquiries", response_model=IdResponse)
async def create_inquiry(inquiry: Inquiry):
    try:
        inserted_id = create_document("inquiry", inquiry)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/inquiries")
async def list_inquiries(limit: int = 50):
    try:
        docs = get_documents("inquiry", {}, limit)
        for d in docs:
            d["id"] = str(d.pop("_id"))
            for k, v in list(d.items()):
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
