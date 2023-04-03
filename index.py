from flask import Flask
from supabase import create_client, Client
import requests

app = Flask(__name__)

url: str = "https://btqrhxskatfcyasskvtz.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0cXJoeHNrYXRmY3lhc3NrdnR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjQ2NjMxODQsImV4cCI6MTk4MDIzOTE4NH0.c2A5FcLIQEvFfAkMg1Fmw_iZQ2SIB6BOxahqnHEA_oM"

y1_model_execute = "https://us-central1-excellent-zoo-381900.cloudfunctions.net/execute_model_y1"
y2_model_execute = "https://us-central1-excellent-zoo-381900.cloudfunctions.net/execute_model_y2"

supabase: Client = create_client(url, key)


@app.route('/')
def home():
    return 'Home'


@app.route('/execute_model_y1')
def about():
    response = (supabase.table('data').select("T_inj_control, GG_rpm, HP_T_exit_temp, timestamp").order(
        column="timestamp", desc=True).limit(1).single().execute()).data

    payload = {"values": [[response["T_inj_control"],
                           response["GG_rpm"], response["HP_T_exit_temp"]]]}

    result = requests.post(y1_model_execute, json=payload)

    supabase.table('predict_outputs').insert(
        {"value": result.text, "timestamp": response["timestamp"], "model_output_name": "y1"}).execute()

    return result.text


@app.route('/execute_model_y2')
def execute():
    response = (supabase.table('data').select("T_inj_control, GG_rpm, HP_T_exit_temp, timestamp").order(
        column="timestamp", desc=True).limit(1).single().execute()).data

    payload = {"values": [[response["T_inj_control"],
                           response["GG_rpm"], response["HP_T_exit_temp"]]]}

    result = requests.post(y2_model_execute, json=payload)

    supabase.table('predict_outputs').insert(
        {"value": result.text, "timestamp": response["timestamp"], "model_output_name": "y2"}).execute()

    return result.text
