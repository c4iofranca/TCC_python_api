from flask import Flask
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL="https://btqrhxskatfcyasskvtz.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0cXJoeHNrYXRmY3lhc3NrdnR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjQ2NjMxODQsImV4cCI6MTk4MDIzOTE4NH0.c2A5FcLIQEvFfAkMg1Fmw_iZQ2SIB6BOxahqnHEA_oM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    response = supabase.table('tag').select("*").execute()
    
    return response.data

@app.route('/about')
def about():
    return 'About'