from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils import db
from utils.sms import AfricasTalking
import urllib.parse
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
origins = [
    os.environ.get("FRONTEND_URL"),
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
    return {"app": "Money share", "status": "ok"}


# UNCOMMENT FOR POSTMAN TESTING
# class Request1(BaseModel):
#     from_: list[str] = Field(..., alias="from")
#     to: list[str]
#     text: list[str]
# POSTMAN TESTING


# SMS
@app.post("/sms")
async def receive_sms(request: Request):
    decoded_string = await request.body()
    parsed_dict = urllib.parse.parse_qs(decoded_string.decode("utf-8"))

    # REPLACE THE ABOVE FOR POSTMAN TESTING
    # async def receive_sms(request: Request1):
    #     parsed_dict = dict(request)
    #     parsed_dict["from"] = request.from_
    #     del parsed_dict["from_"]
    # POSTMAN TESTING

    print(parsed_dict)
    sender_account = db.get_account(parsed_dict["from"][0])
    print(sender_account)
    response = ""
    if not sender_account and "create" not in parsed_dict["text"][0].lower():
        response = (
            f'You do not have an account. To create an account send "create" to 50506'
        )
    else:
        if "balance" in parsed_dict["text"][0].lower():
            response += f'Balance: NGN {sender_account["balance"]}\nDate: {datetime.now().date()}'
        elif "create" in parsed_dict["text"][0].lower():
            if not sender_account:
                new_account = db.add_account(
                    {
                        "phone_number": parsed_dict["from"][0],
                        "account_number": parsed_dict["from"][0].replace("+", ""),
                    }
                )
                print(new_account)
                response = f'Account created for {new_account["account_number"]}\n\nAccount Number: 0033221456\nBalance: NGN {new_account["balance"]}'
            else:
                response = (
                    f'Account ({sender_account["account_number"]}) already exists'
                )
        else:
            details = (
                parsed_dict["text"][0].lower().split(" ")
            )  # Format -> OPERATION PHONE_NUMBER AMOUNT
            if len(details) > 2:
                details[2] = int(details[2].replace(",", ""))
            reciever_account = db.get_account(details[1])
            transaction_ref = uuid.uuid4()
            print(details)
            print(reciever_account)

            if len(details) < 2:
                response = 'Incorrect format received\nFollow -> "AMOUNT PHONE_NUMBER"'
            elif sender_account and details[2] > sender_account["balance"]:
                response = (
                    f'Insufficient funds\nBalance: NGN {sender_account["balance"]}'
                )
            elif "send" in parsed_dict["text"][0].lower() and not reciever_account:
                new_account = db.add_account(
                    {
                        "phone_number": details[1],
                        "account_number": details[1].replace("+", ""),
                        "balance": details[2],
                    }
                )
                updated_sender_account = db.update_account(
                    sender_account["id"],
                    {"balance": sender_account["balance"] - details[2]},
                )

                updated_receiver_account = db.update_account(
                    new_account["id"],
                    {"balance": new_account["balance"]},
                )

                receiver_response = f'Welcome to Money Share banking app. You Received: NGN {details[2]}\nFrom: {sender_account["phone_number"]}\nBalance: NGN {updated_receiver_account[0]["balance"]}.\n\n Send "help" to 50506 to see what actions you can take'
                AfricasTalking().send(
                    os.environ.get("SMS_SHORTCODE"),
                    receiver_response,
                    [updated_receiver_account[0]["phone_number"]],
                )
                print(receiver_response)
                response = f'Account created for {new_account["phone_number"]}\n\nSent: NGN {details[2]}\nTo: {new_account["phone_number"]}\nRef: {transaction_ref}\nBalance: NGN {updated_sender_account[0]["balance"]}'

            elif "send" in parsed_dict["text"][0].lower():
                updated_sender_account = db.update_account(
                    sender_account["id"],
                    {"balance": sender_account["balance"] - details[2]},
                )
                updated_receiver_account = db.update_account(
                    reciever_account["id"],
                    {"balance": reciever_account["balance"] + details[2]},
                )
                receiver_response = f'You Received: NGN {details[2]}\nFrom: {sender_account["phone_number"]}\nBalance: NGN {updated_receiver_account[0]["balance"]}.'
                print("--------2")
                print(details[2], os.environ.get("SMS_SHORTCODE"))
                print(receiver_response)
                print("--------")
                AfricasTalking().send(
                    os.environ.get("SMS_SHORTCODE"), receiver_response, [details[1]]
                )
                response = f'You Sent: NGN {details[2]}\nTo: {details[1]}\nRef: {transaction_ref}\nBalance: NGN {updated_sender_account[0]["balance"]}'
            # elif len(details) == 4:
            #     narration = f"Narration: {details[3]}" if len(details) == 4 else ""
            #     response += f"""
            #     Name: Al-Ameen Abdullahi\n
            #     Sent: NGN {details[3]}\n
            #     To: {details[0]} {details[1]}\n
            #     {narration}\n
            #     Ref: {transaction_ref}\n
            #     Balance: NGN 21,000,000,000,000\n
            #     """

    print(response)
    # return {"response": response}

    AfricasTalking().send(
        os.environ.get("SMS_SHORTCODE"), response, parsed_dict["from"]
    )
