import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.auth.auth_utils import token_generator, token_get_user_id
from app.models import User, db
from app import create_app
app = create_app()

from unittest import TestCase

os.environ['SECRET_KEY'] = "asdfsdf"


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        
        user = User(
            id = 1,
            username="joen",
            email="joen@gmail.com",
            first_name="Joene",
            last_name="Smith",
            password="$2b$12$Ae6.SljpHvGGxyo5WmEte.r3zukiA0H5AeiPLEkZiH9z6fOqp.q7i",
            image_url=None
        )

        db.session.add(user)
        db.session.commit()
        self.user = User.query.get(1)

    def tearDown(self):
        User.query.delete()
        db.session.commit()

    def test_token(self):    
        token = token_generator(self.user)
        self.assertEqual(token_get_user_id(token), 1)

    # register page
    def test_register_page(self):
        with self.client:
            res = self.client.get("/register")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="mt-5">Create an Accout</h1>', html)

    # send data for registiration
    def test_register_with_valid_data(self):
        with self.client:
            res = self.client.post("/register",
                data={'username': "anna", 'email': "ann@gmail.com", 'first_name': "Anna", 'last_name': "Smith",
                     'password': "123456", "confirm": "123456"}, follow_redirects=False)
          
            self.assertEqual(res.status_code, 302)

    # send unvalid data for registiration
    # username aldready exist
    def test_register_with_exist_username(self):
        with self.client:
            res = self.client.post("/register",
                data={'username': "joen", 'email': "joel@gmail.com", 'first_name': "Jne", 'last_name': "Lalle",
                     'password': "123456", "confirm": "123456"})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<span class="text-danger">Username Already Exists</span>', html)

    # send data for registiration
    # email already exist
    def test_register_with_exist_email(self):
        with self.client:
            res = self.client.post("/register",
                data={'username': "joene", 'email': "joen@gmail.com", 'first_name': "Joe", 'last_name': "Same",
                     'password': "123456", "confirm": "123456"})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<span class="text-danger">Email Already Exists</span>', html)

    # send data for registiration
    def test_register_with_invalid_email(self):
        with self.client:
            res = self.client.post("/register",
                data={'username': "smith", 'email': "joe@g", 'first_name': "Jale", 'last_name': "Smith",
                     'password': "123456", "confirm": "123456"})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<span class="text-danger">Invalid email address.</span>', html)

    # open login page
    def test_login_page(self):
        with self.client:
            res = self.client.get("/login")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="mt-5">Login</h1>', html)

    # login user        
    def test_login_with_exist_user(self):
        with self.client:
            res = self.client.post("/login",
                data={'username': "joen",'password': "1234567"})
            self.assertEqual(res.status_code, 302)

    # login user with not exist user     
    def test_login_with_not_exist_user(self):
        with self.client:
            res = self.client.post("/login",
                data={'username': "asdf",'password': "1234567"})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Invalid Username or Password', html)


