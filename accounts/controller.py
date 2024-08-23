from dotenv import load_dotenv
from db.controller import db
from users.schemas import UserType

load_dotenv()


class Account:

    def __init__(self):
        self.db = db

    def create(self, user: UserType):
        try:
            response = (
                self.db.table("accounts")
                .insert(
                    {
                        "account_number": user.phone_number.replace("+234", ""),
                        "user_id": user.id,
                    }
                )
                .execute()
            )
            return [True, response.data[0]]
        except Exception as error:
            print(error)
            return [False, "Account creation failed"]
