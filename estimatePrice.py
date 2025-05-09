import json

with open('values.json', 'r') as file:
    model = json.load(file)

theta0: float = model['theta0']
theta1: float = model['theta1']
min: float = model['min']
range: float = model['rangeKm']

def estimatePrice(km: int):
	global min, range
	price: float
	if (range == 0):
		price = theta1 * km + theta0
	else:
		normalizedKm: float = (km - min) / range
		price = theta1 * normalizedKm + theta0
	print("price: ", price)

try:
	km: float = float(input("Enter a mileage: "))
	estimatePrice(km)
except:
    print("Error: Input must be a number")