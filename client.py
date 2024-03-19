import requests

response = requests.post(
    "http://localhost:5000/user",
    json={"password": "1234fgwesge35235", "name": "user_2",
          "second_name": "second_name_user_1", "mail": "ldldl@inbox.ru"},
)

print(response.text)
print(response.status_code)

response = requests.get(
    "http://localhost:5000/user/1",
   headers={"user_id": "1", "password": "1234fgwesge35235"}
)

print(response.text)
print(response.status_code)

response = requests.post(
    "http://localhost:5000/ad",
    json={"title": "title_1", "description": "description ad_1", "user_id": 1},
)

print(response.text)
print(response.status_code)

response = requests.get(
    "http://localhost:5000/ad/2",
    headers={"authorization": "1234fgwesge35235"}
)

print(response.text)
print(response.status_code)

response = requests.get(
    "http://localhost:5000/ad/2",
#    headers={"authorization": "1234fgwesge35235"}
)

print(response.text)
print(response.status_code)

response = requests.post(
    "http://localhost:5000/ad",
    json={"title": "title_1", "description": "description ad_1", "user_id": 1},
)

print(response.text)
print(response.status_code)

response = requests.post(
    "http://localhost:5000/ad",
    json={"title": "title_1", "description": "description ad_1", "user_id": 1},
    headers={"authorization": "1234fgwesge35235"}
)

print(response.text)
print(response.status_code)

response = requests.get(
    "http://localhost:5000/ad/1",

)

print(response.text)
print(response.status_code)

response = requests.get(
    "http://localhost:5000/ad/10",

)

print(response.text)
print(response.status_code)

response = requests.patch(
    'http://localhost:5000/ad/1',
    json={"title": "ad_1_change"},
    headers={"authorization": "1234fgwesge35235"}
)
print(response.text)
print(response.status_code)

response = requests.patch(
    'http://localhost:5000/ad/1',
    json={"title": "ad_1_change"}
)
print(response.text)
print(response.status_code)

response = requests.delete(
    'http://localhost:5000/ad/1',
)
print(response.text)
print(response.status_code)

response = requests.delete(
    'http://localhost:5000/ad/1',
    headers={"authorization": "1234fgwesge35235"}
)
print(response.text)
print(response.status_code)

response = requests.post(
    "http://localhost:5000/user",
    json={"password": "1234fgwesge35235", "name": "user_1",
          "second_name": "second_name_user_1"},
)

print(response.text)
print(response.status_code)

response = requests.get(
     'http://localhost:5000/user/100',
 )
print(response.text)
print(response.status_code)


response = requests.patch(
    'http://localhost:5000/user/1',
    json={"name": "user_1_change"}
)
print(response.text)
print(response.status_code)

response = requests.get(
    'http://localhost:5000/user/1',
)
print(response.text)
print(response.status_code)


response = requests.delete(
    'http://localhost:5000/user/2',
)
print(response.text)
print(response.status_code)
