# Food Recipe Web App

A web application that people can share their own recipes with has their own account and follow the other users for easy to access their favorite cooker's recipes via following.

This web application provides many recipes that are added by other users and recipes show servings, cooking time, preparation time, and approximate calories per serving.
Recipes are easily accessible under certain categories and can be searchable with queries on the search box.

### Features

-   Users can register on the website and have their own account sharing their own recipes.
-   The user can follow the other users and has to log in to the web app to be able to follow.
-   Users can change their image URL, first name, and last name on their profile.
-   Users can edit or delete their own recipes.
-   Anonymous users can access to all recipes for cooking and search the recipes.
-   User can add their recipes under a certain categories and enter serving, cooking time and preparation time information.
-   Approximate calories calculate automaticly using ingredient list when user add recipe.
-   Show approximate calories for per serving on recipe description.
-   Showing owner name and recipes count of owner under per recipes.
-   User can easily access own profile page from navbar.

### External APIs

Calorie will be calculated using **[external API](https://api-ninjas.com/api/nutrition)**.

### Using Technologies in This Project

-   Python/Flask, Jinja
-   RESTful APIs
-   PostgreSQL, SQLAlchemy,
-   JavaScript, Axios, JQuery, HTML, CSS
-   Heroku
-   Some Libraries using with Flask:

    -   Flask-Login for authentication
    -   Flask-Migrate for create migrations
    -   Flask-Mail for reset password
    -   Flask-WTF for creating and validationg forms
    -   Flask-Bcrypt for create secure password using hashing

-   Flask Blueprint for organize the application with defines a collection of views, templates, static files.
-   Created different config setting for development, production and testing enviroments.

### Project Demo Link

You can check my food web application from here!

https://food-recipe-web-app.herokuapp.com/

### DEVELOPMENT

##### Test

Change Enviroment

```
$ export FLASK_ENV=test
```

Run all test in test file.

```
$python -m unittest discover app.test
```

#### Deploy

```
$git push heroku main
```
