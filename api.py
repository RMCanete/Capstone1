import requests
# resp = requests.get("https://itunes.apple.com/search", params={"term": "billy bragg", "limit": 3})
# print(resp.json())

res = requests.get("http://www.thecocktaildb.com/api/json/v1/1/search.php?", params={"key": 1, "s": 'tequila'})

data = res.json()

for drink in data['drinks']:
    print(drink['strDrink'])
    print(drink['strInstructions'])
    print(drink['strDrinkThumb'])
    for i in range(1,16):
        if f'strIngredient{i}' == None:
            print("###############################")
        else:
            print(drink[f"strIngredient{i}"])
            print(drink[f"strMeasure{i}"])


