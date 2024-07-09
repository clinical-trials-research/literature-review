import httpx

API_BASE = "https://clinicaltrials.gov/api/v2"
API_FIELD_VALUES = API_BASE + "/stats/field/values"

response = httpx.get(API_FIELD_VALUES)
pieces = [i["piece"] for i in response.json()]

with open("./files/fields.txt", "w") as f:
    for i in pieces:
        f.write(f"{i}\n")
