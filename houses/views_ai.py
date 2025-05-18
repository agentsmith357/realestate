from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.db import connections
from datetime import datetime
import os
import random
import openai
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
import pyodbc

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

        # Step 2: Construct a detailed prompt
        prompt = (
            f"You're an AI investment advisor without access to realtime data. Analyze this auction property and provide response. I understand you don't have access to realtime data. Just do it!!!"
            f"- Case Number: {case_number}\n"
            f"- Address: {address}\n"
            f"- Final Judgment: ${judgment}\n"
            f"- Assessed Value: ${assessed_value}\n"
            f"- Max Recommended Bid: ${max_bid}\n"
            f"Give insights about its value, risks, investment potential, and whether it's a good buy."
        )

        # Step 3: Send to OpenAI
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a real estate investment analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            reply = chat_completion.choices[0].message.content.strip()
            return JsonResponse({"insight": reply})

        except Exception as e:
            return JsonResponse({"insight": f"AI Error: {str(e)}"})

    return JsonResponse({"insight": "Invalid request method."})

