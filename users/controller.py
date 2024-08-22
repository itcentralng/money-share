import os
from supabase import create_client
from dotenv import load_dotenv
from users.schemas import UserType
from response_templates.create_tmpl import (
    create_exists_template,
    create_failed_template,
)

load_dotenv()

db = create_client(
    supabase_key=os.environ.get("SUPABASE_KEY"),
    supabase_url=os.environ.get("SUPABASE_URL"),
)


class User:

    def __init__(self):
        self.db = db

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
                return [False, create_failed_template]
