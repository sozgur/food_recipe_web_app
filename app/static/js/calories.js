$calculateCaloriesButton = $("#calculateCalories");

async function calculateCalories(ingredients) {
    const res = await axios({
        url: "/calculate-calories/json",
        method: "POST",
        data: { ingredients },
    });

    return res.data.calories;
}

async function updateCalories(evt) {
    evt.preventDefault();
    const ingredientLines = $("#ingredients").val().split("\n");
    let ingredients = "";
    for (let i = 0; i < ingredientLines.length; i++) {
        ingredients = ingredients.concat(ingredientLines[i], ", ");
    }
    console.log(ingredients);
    const calories = await calculateCalories(ingredients);
    console.log(calories);

    if (calories) {
        $("#calories").val(calories);
        $("#calories-info").text(calories);
        console.log(calories);
    }
}

$calculateCaloriesButton.on("click", updateCalories);
