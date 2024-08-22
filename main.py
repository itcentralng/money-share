from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sms.models import SMSModel
from dotenv import load_dotenv
from response_templates.help_tmpl import (
    help_template,
    help_create_template,
    help_info_template,
    help_send_template,
)

load_dotenv()
app = FastAPI()
origins = [
    "*",
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
    command, *segments = sms.text.split(" ")

    # HELP COMMANDS
    match command.lower():
        case "help":
            if not len(segments):
                return help_template
            else:
                match segments[0]:
                    case "info":
                        return help_info_template
                    case "create":
                        return help_create_template
                    case "send":
                        return help_send_template

    return [command, segments]
