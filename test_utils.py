# Generated from Postman
import requests
import json

# Create list
url = "localhost:5000/api/todolist/"

payload = json.dumps({
  "title": "List1"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# Create Task
url = "localhost:5000/api/todolist/1/task"
payload = json.dumps({
  "title": "buy biscuits",
  "description": "remember to buy this for everyone",
  "due_at": "2021-04-28 00:12:00"
})
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

# Update List
url = "localhost:5000/api/todolist/1/"
payload = json.dumps({
  "title": "groceries...2"
})
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("PUT", url, headers=headers, data=payload)
print(response.text)

# Update Task
url = "localhost:5000/api/todolist/1/task/1/"
payload = json.dumps({
  "title": "buy biscuits",
  "description": "remember to buy this for only me",
  "due_at": "2021-04-28 00:12:00",
  "status": "DONE"
})
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("PUT", url, headers=headers, data=payload)
print(response.text)

# Delete Task
url = "localhost:5000/api/todolist/1/task/1/"
payload = json.dumps({
  "task_id": 1
})
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("DELETE", url, headers=headers, data=payload)
print(response.text)

# Get All Pending Tasks
url = "localhost:5000/api/todolist/1/task/pending"
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
