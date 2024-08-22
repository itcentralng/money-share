from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sms.models import SMSModel
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
origins = [
    "https://api.africastalking.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return {"app": "Monee share", "status": "ok"}


@app.post("/incoming-sms")
async def receive_sms(sms: SMSModel):
    print(sms)
    return sms
