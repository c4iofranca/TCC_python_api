from flask import Flask
from supabase import create_client, Client
import pickle

app = Flask(__name__)

SUPABASE_URL = "https://btqrhxskatfcyasskvtz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0cXJoeHNrYXRmY3lhc3NrdnR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjQ2NjMxODQsImV4cCI6MTk4MDIzOTE4NH0.c2A5FcLIQEvFfAkMg1Fmw_iZQ2SIB6BOxahqnHEA_oM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def home():
    return 'Home'


@app.route('/execute_y1_model')
def about():
    with open('model_y1.pkl', 'rb') as f:
        model = pickle.load(f)

    response = (supabase.table('data').select("T_inj_control, GG_rpm, HP_T_exit_temp, timestamp").order(
        column="timestamp", desc=True).limit(1).single().execute()).data

    test = [[response["T_inj_control"],
             response["GG_rpm"], response["HP_T_exit_temp"]]]

    result = model.predict(test)

    supabase.table('predict_outputs').insert(
        {"value": result[0], "timestamp": response["timestamp"], "model_output_name": "y1"}).execute()

    return True
