from supabase import create_client
from django.conf import settings

def get_supabase_client():

    supabase_url = settings.SUPABASE_URL
    supabase_api_key = settings.SUPABASE_API_KEY
    return create_client(supabase_url, supabase_api_key)
