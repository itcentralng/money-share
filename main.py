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
from response_templates.create_tmpl import create_user_template, create_failed_template
from users.controller import User
from users.schemas import UserType

load_dotenv()
app = FastAPI()
user_db = User()

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

    match command.lower():
        case "create":
            user = user_db.create(UserType(phone_number=sms.from_, pin="1234"))
            if user[0]:
                return create_user_template.format(account_number=user)
            else:
                return user[1]

    match command.lower():
        case "info":
            user = user_db.get(UserType(phone_number=sms.from_, pin="1234"))
            if user[0]:
                return create_user_template.format(account_number=user)
            else:
                return user[1]

    return [command, segments]
