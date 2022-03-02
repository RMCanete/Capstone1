import requests


# res = requests.get("http://www.thecocktaildb.com/api/json/v1/1/search.php?", params={"key": 1, "s": 'tequila'})

# data = res.json()

# for drink in data['drinks']:
#     print(drink['strDrink'])
#     print(drink['strInstructions'])
#     print(drink['strDrinkThumb'])
#     for i in range(1,16):
#         if f'strIngredient{i}' == None:
#             print("###############################")
#         else:
#             print(drink[f"strIngredient{i}"])
            # print(drink[f"strMeasure{i}"])


res = requests.get("http://www.thecocktaildb.com/api/json/v1/1/search.php?", params={"key": 1, "s": 'tequila'})

data = res.json()
output = []

for drink in data['drinks']:

    name = (drink['strDrink'])
    instructions = (drink['strInstructions'])
    image = (drink['strDrinkThumb'])
    ingredient = []
    measurement = []
    for i in range(1,5):
        ingredient.append(drink[f"strIngredient{i}"])
        measurement.append(drink[f"strMeasure{i}"])

    drink = {'name':name, 'instructions':instructions, 'image':image, 'ingredient': ingredient, 'measurement': measurement, 'Next': '####################################################################################################################'}
    output.append(drink)
print(output)



# search = request.args.get('s')