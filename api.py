import requests

base_url="https://www.thecocktaildb.com/api/json/v1/1"


async def get_drinks_by_name(name):
    res = await requests.get(f"{base_url}/search.php", params={"s": name})
    return res.json()["drinks"][0]

async def get_drink_by_id(id):
    res = await requests.get(f"{base_url}/lookup.php", params={"i": id})
    return res.json()["drinks"][0]

async def get_random_cocktail():
    res = await requests.get(f"{base_url}/random.php")
    return res.json()["drinks"][0]
