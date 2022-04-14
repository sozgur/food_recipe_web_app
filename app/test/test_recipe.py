import os
from app.models import Recipe, User, db
from app import create_app
app = create_app()

from unittest import TestCase
from flask_login import login_user
from flask import session

#Set the session cookie on the client, so Flask can load the same session for the request
def set_session_cookie(client):
    val = app.session_interface.get_signing_serializer(app).dumps(dict(session))
    client.set_cookie('localhost', app.session_cookie_name, val)

os.environ['SECRET_KEY'] = "asdfsdf"

class RecipeTestCase(TestCase):

    def setUp(self):
        self.client = app.test_client()


        self.user = User(
            username="joen",
            email="joen@gmail.com",
            first_name="Joene",
            last_name="Smith",
            password="$2b$12$Ae6.SljpHvGGxyo5WmEte.r3zukiA0H5AeiPLEkZiH9z6fOqp.q7i",
            image_url=None
        )
        

        db.session.add(self.user)
        db.session.commit()
      

    def tearDown(self):
        User.query.delete()
        Recipe.query.delete()
        db.session.commit()

    # open recipe page with authenticated user
    def test_open_add_recipe_page(self):
        with app.test_request_context(), app.test_client() as test_client: 
            login_user(self.user)
            self.user.authenticated = True

            set_session_cookie(test_client)  # Add this
            res = test_client.get("/add-recipe")
            self.assertEqual(res.status_code, 200)


    # can not open recipe page with unauthenticated user
    # redirect login page
    def test_add_recipe_page(self):
        with self.client: 
            res = self.client.get("/add-recipe", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="mt-5">Login</h1>', html)


    def test_successfully_adding_recipe(self):
        with app.test_request_context(), app.test_client() as test_client: 
            login_user(self.user)
            self.user.authenticated = True
            set_session_cookie(test_client)
            res = test_client.post("/add-recipe",
                data={'title': "Cake", 
                      'ingredients':"1 1/2 cups sugar, 2 eggs, pinch salt, 2 cup sour milk",
                      'directions': "Mix all ingredients together.",
                      'category': '1',
                      'image_url': None,
                      'calories': None,
                      'prep': '5 mins',
                      'cook': '5 mins',
                      'servings': '12'
                   }, follow_redirects=True)

            html = res.get_data(as_text=True)
            self.assertIn('<h4>Cake</h4>', html)
            

