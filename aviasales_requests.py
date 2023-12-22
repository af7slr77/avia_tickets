import requests
from config import token
import json

headers = {
	"X-Access-Token": token
}

def get_iata_code(city_name):
	city_name = city_name.strip()
	with open("cities.json", "r") as f:
		cities = json.load(f)
		for elm in cities:
			if city_name.lower() == elm["name"].lower():
				iata_code = elm["code"]
				return iata_code
		return {"msg": "city not found"}

def get_ticket(args):
	city_of_departure = args["city_of_departure"]
	destination_city = args["destination_city"]
	domain = "https://api.aviasales.ru"
	direct_url = f"/v1/cities/{city_of_departure}/directions/{destination_city}/prices/direct.json"
	transfer_url = f"/v1/cities/{city_of_departure}/directions/{destination_city}/prices.json"
	calendar = f"/v1/cities/{city_of_departure}/directions/{destination_city}/prices/calendar.json"

	params = {
		"departure_at": args['departure_at'],
		"return_at": args['return_at'],
	}
	if args['transfer'] is not None:
		url = domain + transfer_url
		res = requests.get(url=url, headers=headers, params=params)
		return res.json()
	if args["get_calendar"] is not None:
		url = domain + calendar
		res = requests.get(url=url, headers=headers, params=params)
		return res.json()
	url = domain + direct_url
	res = requests.get(url=url, headers=headers, params=params)
	return res.json()
