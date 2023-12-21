import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_account(phone_number):
    try:
        print()
        response = (
            supabase.table("users")
            .select("*")
            .eq("phone_number", phone_number)
            .execute()
        )
        if len(response.data):
            return response.data[0]
        else:
            return None
    except Exception as error:
        print(error)
        return None


def update_account(id, details):
    try:
        print()
        response = supabase.table("users").update(details).eq("id", id).execute()
        if len(response.data):
            return response.data
        else:
            return None
    except Exception as error:
        print(error)
        return None


def add_account(details):
    keys_to_check = [
        # "full_name",
        "phone_number",
        "account_number",
        # "pin",
    ]
    all_exist = all(key in details for key in keys_to_check)

    if all_exist:
        try:
            response = supabase.table("users").insert(details).execute()

            if len(response.data):
                return response.data[0]
            else:
                return None
        except Exception as error:
            print(error)
            return None
    else:
        print("Some required keys are missing.")
        return {"error": "Some required keys are missing."}
