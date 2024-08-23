import os
from supabase import create_client

db = create_client(
    supabase_key=os.environ.get("SUPABASE_KEY"),
    supabase_url=os.environ.get("SUPABASE_URL"),
)
