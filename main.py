from fastapi import FastAPI, Request, HTTPException

import logging

from logging.handlers import RotatingFileHandler

from transformers import get_transformer

from mis_service import send_to_mis
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Logging setup
handler = RotatingFileHandler(
    "app.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3
)

logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI(
    title="SM Filter Bot API",
    root_path="/sm_filter_bot"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/leads")
async def receive_lead(request: Request):

    # 🔹 Safe JSON parsing
    try:

        incoming = await request.json()

    except Exception:

        logging.error("INVALID JSON RECEIVED")

        raise HTTPException(
            400,
            "Invalid JSON"
        )

    source = incoming.get("source")

    if not source:

        logging.error("MISSING SOURCE")

        raise HTTPException(
            400,
            "Source required"
        )

    data = incoming.get("data", {})

    transformer = get_transformer(source)

    if not transformer:

        logging.error(
            f"UNKNOWN SOURCE | SOURCE={source}"
        )

        raise HTTPException(
            400,
            f"Unknown source: {source}"
        )

    payload = transformer(data)

    logging.info(
        f"RECEIVED | SOURCE={source} | DATA={payload}"
    )

    try:

        # ✅ IMPORTANT CHANGE
        await send_to_mis(payload)

    except Exception as e:

        logging.error(
            f"MIS FAILURE | "
            f"ERROR={str(e)} | "
            f"DATA={payload}"
        )

        raise HTTPException(
            500,
            "MIS API failed"
        )

    return {
        "status": "success"
    }


# ✅ VERIFICATION (GET)

VERIFY_TOKEN = "123456"

@app.get("/webhook")

async def verify_webhook(request: Request):

    params = request.query_params

    mode = params.get("hub.mode")

    challenge = params.get("hub.challenge")

    verify_token = params.get("hub.verify_token")

    if mode == "subscribe" and verify_token == VERIFY_TOKEN:

        return int(challenge)  # IMPORTANT: return raw challenge

    raise HTTPException(status_code=403, detail="Verification failed")

# ✅ RECEIVE EVENTS (POST)

@app.post("/webhook")

async def receive_webhook(request: Request):

    body = await request.json()

    print("🔥 WEBHOOK HIT")

    print(body)

    return {"status": "ok"}  # IMPORTANT: must return 200