import requests

res = requests.post("http://127.0.0.1:8080/group", {"name": "group1", "description": "Group1"})
res = requests.post("http://127.0.0.1:8080/group", {"name": "group2", "description": "Group2"})
res = requests.get("http://127.0.0.1:8080/groups")
res = requests.get("http://127.0.0.1:8080/group/1")
res = requests.put("http://127.0.0.1:8080/group/2", {"name": "group2_1", "description": "Group2_1"})
res = requests.delete("http://127.0.0.1:8080/group/2")
res = requests.post("http://127.0.0.1:8080/group/1/participant", {"name": "part1", "wish": "prize"})
res = requests.post("http://127.0.0.1:8080/group/1/participant", {"name": "part2", "wish": "prize"})
res = requests.post("http://127.0.0.1:8080/group/1/participant", {"name": "part3", "wish": "prize"})
res = requests.post("http://127.0.0.1:8080/group/1/participant", {"name": "part4", "wish": "prize"})
res = requests.delete("http://127.0.0.1:8080/group/1/participant/4")
res = requests.post("http://127.0.0.1:8080/group/1/toss")
res = requests.get("http://127.0.0.1:8080/group/1/participant/1/recipient")
print(res.json())

