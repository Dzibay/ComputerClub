from supabase import create_client
import os

SUPABASE_URL = "https://vmkrbepxuwnhauzrglwd.supabase.co"
SUPABASE_KEY = "sb_secret_7w2rwVY0uYc0wAynOHs6gA_KcYZOm3Y"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
