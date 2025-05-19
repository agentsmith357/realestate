from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.db import connections
from datetime import datetime
import os
import random
import requests
import openai
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
import pyodbc

# Set your RapidAPI Key
rapidapi_key = settings.RAPIDAPI_KEY

headers = {
    "X-RapidAPI-Key": rapidapi_key,
    "X-RapidAPI-Host": ""
}


@csrf_exempt
def ai_audit(request):
    from openai import OpenAI
    client = OpenAI(api_key=settings.AI_KEY)

    if request.method == "POST":
        case_number = request.POST.get("case", "").strip()
        if not case_number:
            return JsonResponse({"insight": "Missing case number."})

        # Step 1: Query the database for auction data
        conn = pyodbc.connect(f"""Driver={settings.MYSQL_DRIVER_NAME};
            Server={settings.MYSQL_IP};
            Database={settings.MYSQL_DB_NAME};
            UID={settings.MYSQL_USER};
            PWD={settings.MYSQL_PASSWORD}""")
        with conn.cursor() as cur:
            cur.execute("""
                SELECT address, final_judgement, assessed_value, max_bid
                FROM houses
                WHERE case_number = ?;
            """, case_number)
            row = cur.fetchone()
        if not row:
            return JsonResponse({"insight": f"No property found for case {case_number}."})

        address, judgment, assessed_value, max_bid = row
        data = gather_real_estate_data(address)

        # Step 2: Construct a detailed prompt
        prompt = (
            f"Analyze the following real estate data for {address}"
            f"- Case Number: {case_number}\n"
            f"- Address: {address}\n"
            f"- Final Judgment: ${judgment}\n"
            f"- Assessed Value: ${assessed_value}\n"
            f"- Max Recommended Bid: ${max_bid}\n"
            f"- Audit data: {data}"
        )
        print(prompt)

        # Step 3: Send to OpenAI
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a real estate investment analyst."},
                    {"role": "user", "content":prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            reply = chat_completion.choices[0].message.content.strip()
            return JsonResponse({"insight": reply})

        except Exception as e:
            return JsonResponse({"insight": f"AI Error: {str(e)}"})

    return JsonResponse({"insight": "Invalid request method."})



# Zillow Example
def get_zillow_data(location):
    url = "https://zillow56.p.rapidapi.com/search"
    headers["X-RapidAPI-Host"] = "zillow56.p.rapidapi.com"
    params = {"location": location}
    response = requests.get(url, headers=headers, params=params)
    return {"source": "Zillow", "data": str(response.json())}

# Realtor Example
def get_realtor_data(location):
    url = "https://realtor.p.rapidapi.com/locations/auto-complete"
    headers["X-RapidAPI-Host"] = "realtor.p.rapidapi.com"
    params = {"input": location}
    response = requests.get(url, headers=headers, params=params)
    return {"source": "Realtor", "data": str(response.json())}

# Mashvisor (if available)
def get_mashvisor_data(location):
    url = "https://mashvisor-api.p.rapidapi.com/rental-rates"
    headers["X-RapidAPI-Host"] = "mashvisor-api.p.rapidapi.com"
    params = {"state": "FL", "city": location.split(",")[0]}
    response = requests.get(url, headers=headers, params=params)
    return {"source": "Mashvisor", "data": str(response.json())}

# Combine all data
def gather_real_estate_data(location):
    sources = [
        get_zillow_data(location),
       # get_realtor_data(location),
       #get_mashvisor_data(location)
    ]
    combined = "\n".join([f"{s['source']}: {s['data']}" for s in sources])
    return combined
