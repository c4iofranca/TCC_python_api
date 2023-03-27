from flask import Flask
from supabase import create_client, Client
import os
import requests

app = Flask(__name__)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

y1_model_execute = os.environ.get("GOOGLE_CLOUD_MODEL_Y1_URL")

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
