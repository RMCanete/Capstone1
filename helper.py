from models import Drink,Ingredient,DrinkIngredient,db

def parse_drink(drink):
    added_drink= Drink(id=drink['idDrink'],name=drink['strDrink'],instructions=drink['strInstructions'],image=drink['strDrinkThumb'])
    ingredients=[]
    drink_ingredients=[]
    for i in range(1,16):
        ingredient_name=drink.get(f"strIngredient{i}",None)
        ingredient_measure=drink.get(f"strMeasure{i}",None)
        if ingredient_name:
            ingredient_exists= check_for_ingredient(ingredient_name)
            if not ingredient_exists:
                ingredient=Ingredient(name=ingredient_name)
                ingredients.append(ingredient)
            else:
                ingredient=ingredient_exists
            if ingredient_measure:
                ingredient_measure=ingredient_measure.strip()
                measurment=ingredient_measure.split(" ")[-1]
                quantity=" ".join(ingredient_measure.split(" ")[0:-1])
            else:
                measurment=None
                quantity=None
            drink_ingredients.append(DrinkIngredient(drink_id=added_drink.id,ingredient_id=ingredient.id,quantity=quantity,measurement_unit=measurment))

        else:
            break
    return {"drink":added_drink, "ingredients":ingredients,"drink_ingredients":drink_ingredients}


def check_for_drink(id):
    drinks=Drink.query.filter_by(id=id)
    if drinks.count()==0:
        return False
    return True

def check_for_ingredient(name):
    ingredients=Ingredient.query.filter_by(name=name)
    if ingredients.count()==0:
        return False
    return ingredients[0]

def add_drink(drink):
    if not check_for_drink(drink["idDrink"]):
        result = parse_drink(drink)
        db.session.add(result["drink"])
        db.session.bulk_save_objects(result["ingredients"])
        db.session.bulk_save_objects(result["drink_ingredients"])
        db.session.commit()
        return True
    return False
        