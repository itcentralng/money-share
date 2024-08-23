from dotenv import load_dotenv
from db.controller import db
from users.schemas import UserType
from response_templates.create_tmpl import (
    create_exists_template,
    create_failed_template,
)
from response_templates.account_tmpl import (
    account_info_template,
    account_not_found_template,
)

load_dotenv()


class User:

    def __init__(self):
        self.db = db
        # self.user = None

    def create(self, user: UserType):
        try:
            response = (
                self.db.table("users")
                .insert({"phone_number": user.phone_number, "pin": user.pin})
                .execute()
            )
            return [True, response.data[0]]
        except Exception as error:
            if "duplicate" in error.__dict__.get("message"):
                return [False, create_exists_template]
            else:
                print(error)
                return [False, create_failed_template]

    def get(self, user: UserType):
        print(user)
        try:
            response = (
                self.db.table("users")
                .select("*")
                .eq("phone_number", user.phone_number)
                .execute()
            )
            if len(response.data):
                return [True, response.data[0]]
            else:
                return [False, account_not_found_template]
        except Exception as error:
            print(error)
            return [False, account_not_found_template]
