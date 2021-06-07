import requests

url = "http://localhost:5000/api/games/1"

r = requests.get(url)
print(r.json())
