function createDrinkHTML(drink) {
    return `<div>
      <li data-id="${drink.drink_id}">
        <img class="image img-thumbnail" src="${drink.drink_image}">
        Ingredients: ${drink.drink_ingridents_id}, Instructions: ${drink.drink_instructions}
        <button class="view-drink btn-sm btn-danger">View</button>
      </li>
    </div>`;
  }
  
async function showFavoritesList() {
  const response = await axios.get(`http://127.0.0.1:5000/show_favorites`);    
  for (let favorites of response.data.favorites) {
    let favorite = $(createDrinkHTML(favorites));
    $("#favorites-list").append(favorite);
  }
}

async function showDrinksList() {
    const response = await axios.get(`www.thecocktaildb.com/api/json/v1/1`);    
    for (let drinks of response.data.drinks) {
      let drink = $(createDrinkHTML(drinks));
      $("#drinks-list").append(drink);
    }
  }

showFavoritesList();
showDrinksList();