from datetime import datetime,timedelta
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pyodbc
from django.http import JsonResponse
from django.conf import settings


# LOGIN ATTEMPT — set cookie with username
@csrf_exempt
def login_attempt(request):
    if request.method == "GET":
        return render(request, "index.html")
    else:
        conn = pyodbc.connect(f"""Driver={settings.MYSQL_DRIVER_NAME};
            Server={settings.MYSQL_IP};
            Database={settings.MYSQL_DB_NAME};
            UID={settings.MYSQL_USER};
            PWD={settings.MYSQL_PASSWORD}""")
        with conn.cursor() as cur:
            cur.execute("""
                SELECT username FROM account 
                WHERE username = ? AND password = ?;
            """, request.POST.get("username"), request.POST.get("password"))
            data = cur.fetchone()

        if data is not None:
            response = JsonResponse({"data": True})
            expires = datetime.strftime(datetime.utcnow() + timedelta(days=3650), "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie("hcp_realstate", request.POST.get("username"), expires=expires)
            return response
        else:
            return JsonResponse({"data": False})
		
first_name = "Jelani"
last_name = "Jenkins"
full_name = first_name + " " + last_name
print("Welcome " + full_name)

@csrf_exempt
def index(request):
	if request.method =="GET":
	    return render(request,"index.html")
		
@csrf_exempt
def login(request):
	if request.method =="GET":
	    return render(request,"signin.html")
	

		
@csrf_exempt
def load_data(request):
	if request.method =="GET":
		return render(request,"index.html")
	else:
		print("connecting to db...")
		conn = pyodbc.connect(f"""Driver={settings.MYSQL_DRIVER_NAME};
				Server={settings.MYSQL_IP};
				Database={settings.MYSQL_DB_NAME};
				UID={settings.MYSQL_USER};
				PWD={settings.MYSQL_PASSWORD}""")
		print("connected.")
		data= None
		with conn.cursor() as cur:
			cur.execute("""SELECT 
				date
				,auction_status
				,auction_type
				,case_number
				,final_judgement
				,parcel_id
				,address
				,assessed_value
				,max_bid
				,is_watching
				,is_house_sold
				,is_canceled	
				,is_my_watchlist
				FROM houses;""")
			data = cur.fetchall()
		package = [{"date":t[0]
				,"auction_status":t[1]
				,"auction_type":t[2]
				,"case_number":t[3]
				,"final_judgement":t[4]
				,"parcel_id":t[5]
				,"address":t[6]
				,"assessed_value":t[7]
				,"max_bid":t[8]
				,"is_watching":t[9]
				,"is_house_sold":t[10]
				,"is_canceled":t[11]
				,"is_my_watchlist":t[12]

				}
				 for t in data]
	return JsonResponse({'data':package})




@csrf_exempt
def follow(request):
	if request.method =="GET":
		return render(request,"index.html")
	else:
		case =request.POST.get("case")
		if case is not None:

			print("connecting to db...")
			conn = pyodbc.connect(f"""Driver={settings.MYSQL_DRIVER_NAME};
				Server={settings.MYSQL_IP};
				Database={settings.MYSQL_DB_NAME};
				UID={settings.MYSQL_USER};
				PWD={settings.MYSQL_PASSWORD}""")
			print("connected.")
			data= None
			with conn.cursor() as cur:
				cur.execute("""
					update  houses set is_my_watchlist = 1
					where case_number = ?;""",case)
			#with conn.cursor() as cur:
			#	cur.execute("""SELECT 
			#		date
			#		,auction_status
			#		,auction_type
			#		,case_number
			#		,final_judgement
			#		,parcel_id
			#		,address
			#		,assessed_value
			#		,max_bid
			#		,is_watching
			#		,is_house_sold
			#		,is_canceled
			#		FROM houses where is_watching = 1;""")
			#	data = cur.fetchall()
			#package = [{"date":t[0]
			#		,"auction_status":t[1]
			#		,"auction_type":t[2]
			#		,"case_number":t[3]
			#		,"final_judgement":t[4]
			#		,"parcel_id":t[5]
			#		,"address":t[6]
			#		,"assessed_value":t[7]
			#		,"max_bid":t[8]
			#		,"is_watching":t[9]
			#		,"is_house_sold":t[10]
			#		,"is_canceled":t[11]}
			#		for t in data]
	return JsonResponse({'data':'NA'})




@csrf_exempt
def unfollow(request):
	if request.method =="GET":
		return render(request,"index.html")
	else:
		case =request.POST.get("case")
		if case is not None:

			print("connecting to db...")
			conn = pyodbc.connect(f"""Driver={settings.MYSQL_DRIVER_NAME};
				Server={settings.MYSQL_IP};
				Database={settings.MYSQL_DB_NAME};
				UID={settings.MYSQL_USER};
				PWD={settings.MYSQL_PASSWORD}""")
			print("connected.")
			data= None
			with conn.cursor() as cur:
				cur.execute("""
					update  houses set is_my_watchlist = 0
					where case_number = ?""",case)
			#with conn.cursor() as cur:
			#	cur.execute("""SELECT 
			#		date
			#		,auction_status
			#		,auction_type
			#		,case_number
			#		,final_judgement
			#		,parcel_id
			#		,address
			#		,assessed_value
			#		,max_bid
			#		,is_watching
			#		,is_house_sold
			#		,is_canceled
			#		FROM houses where is_watching = 1;""")
			#	data = cur.fetchall()
			#package = [{"date":t[0]
			#		,"auction_status":t[1]
			#		,"auction_type":t[2]
			#		,"case_number":t[3]
			#		,"final_judgement":t[4]
			#		,"parcel_id":t[5]
			#		,"address":t[6]
			#		,"assessed_value":t[7]
			#		,"max_bid":t[8]
			#		,"is_watching":t[9]
			#		,"is_house_sold":t[10]
			#		,"is_canceled":t[11]}
			#		for t in data]
	return JsonResponse({'data':'NA'})



@csrf_exempt
def filter_data(request):
	if request.method =="GET":
		return render(request,"index.html")
	else:
		print("connecting to db...")
		conn = pyodbc.connect(f"""Driver={settings.MYSQL_DRIVER_NAME};
			Server={settings.MYSQL_IP};
			Database={settings.MYSQL_DB_NAME};
			UID={settings.MYSQL_USER};
			PWD={settings.MYSQL_PASSWORD}""")
		print("connected.")
		filter =request.POST.get("filter")
		if filter=="this week":
			data= None
			today = datetime.now()    
			end = today - timedelta(days=-7)

			with conn.cursor() as cur:
				cur.execute("""SELECT 
				date
				,auction_status
				,auction_type
				,case_number
				,final_judgement
				,parcel_id
				,address
				,assessed_value
				,max_bid
				,is_watching
				,is_house_sold
				,is_canceled
					FROM houses where date >= ? and  date <= ?;""",today.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d"))
				data = cur.fetchall()
			package = [{"date":t[0]
					,"auction_status":t[1]
					,"auction_type":t[2]
					,"case_number":t[3]
					,"final_judgement":t[4]
					,"parcel_id":t[5]
					,"address":t[6]
					,"assessed_value":t[7]
					,"max_bid":t[8]
					,"is_watching":t[9]
					,"is_house_sold":t[10]
					,"is_canceled":t[11]}
					for t in data]
		elif filter=="this month":
			data= None
			today = datetime.now()    
			end = today - timedelta(days=-7)

			with conn.cursor() as cur:
				cur.execute("""SELECT 
				date
				,auction_status
				,auction_type
				,case_number
				,final_judgement
				,parcel_id
				,address
				,assessed_value
				,max_bid
				,is_watching
				,is_house_sold
				,is_canceled
				,is_my_watchlist
					FROM houses where date like ?;""",today.strftime("%Y-")+today.strftime("%m-")+ '%')
				data = cur.fetchall()
			package = [{"date":t[0]
					,"auction_status":t[1]
					,"auction_type":t[2]
					,"case_number":t[3]
					,"final_judgement":t[4]
					,"parcel_id":t[5]
					,"address":t[6]
					,"assessed_value":t[7]
					,"max_bid":t[8]
					,"is_watching":t[9]
					,"is_house_sold":t[10]
					,"is_canceled":t[11]
				    ,"is_my_watchlist":t[12]

					}
					for t in data]		
		elif filter=="all":
			data= None
			today = datetime.now()    
			end = today - timedelta(days=-7)

			with conn.cursor() as cur:
				cur.execute("""SELECT 
				date
				,auction_status
				,auction_type
				,case_number
				,final_judgement
				,parcel_id
				,address
				,assessed_value
				,max_bid
				,is_watching
				,is_house_sold
				,is_canceled
				,is_my_watchlist
					FROM houses """)
				data = cur.fetchall()
			package = [{"date":t[0]
					,"auction_status":t[1]
					,"auction_type":t[2]
					,"case_number":t[3]
					,"final_judgement":t[4]
					,"parcel_id":t[5]
					,"address":t[6]
					,"assessed_value":t[7]
					,"max_bid":t[8]
					,"is_watching":t[9]
					,"is_house_sold":t[10]
					,"is_canceled":t[11]
					,"is_my_watchlist":t[12]

					}
					for t in data]		
		elif filter=="watching":
			data= None
			with conn.cursor() as cur:
				cur.execute("""SELECT 
				date
				,auction_status
				,auction_type
				,case_number
				,final_judgement
				,parcel_id
				,address
				,assessed_value
				,max_bid
				,is_watching
				,is_house_sold
				,is_canceled
				,is_my_watchlist
					FROM houses where is_watching = ?;""",'1')
				data = cur.fetchall()
			package = [{"date":t[0]
					,"auction_status":t[1]
					,"auction_type":t[2]
					,"case_number":t[3]
					,"final_judgement":t[4]
					,"parcel_id":t[5]
					,"address":t[6]
					,"assessed_value":t[7]
					,"max_bid":t[8]
					,"is_watching":t[9]
					,"is_house_sold":t[10]
					,"is_canceled":t[11]
					,"is_my_watchlist":t[12]

					}
					for t in data]
		elif filter=="my_items":
			data= None
			with conn.cursor() as cur:
				cur.execute("""SELECT 
				date
				,auction_status
				,auction_type
				,case_number
				,final_judgement
				,parcel_id
				,address
				,assessed_value
				,max_bid
				,is_watching
				,is_house_sold
				,is_canceled
				,is_my_watchlist
					FROM houses where is_my_watchlist = ?;""",'1')
				data = cur.fetchall()
			package = [{"date":t[0]
					,"auction_status":t[1]
					,"auction_type":t[2]
					,"case_number":t[3]
					,"final_judgement":t[4]
					,"parcel_id":t[5]
					,"address":t[6]
					,"assessed_value":t[7]
					,"max_bid":t[8]
					,"is_watching":t[9]
					,"is_house_sold":t[10]
					,"is_canceled":t[11]
					,"is_my_watchlist":t[12]

					}
					for t in data]
	return JsonResponse({'data':package})

@csrf_exempt
def validate_cookie(request):
	username = request.COOKIES.get("hcp_realstate")
	if not username:
		return False
	else:
		return True
