import os
from app.models import User, db
from app import create_app
app = create_app()
from unittest import TestCase

os.environ['SECRET_KEY'] = "asdfsdf"

class ModelTestCase(TestCase):

    def setUp(self):
    
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
        db.session.commit()


    def test_fullname(self):
        self.assertEqual(self.user.fullname, "Joene Smith")

    def test_image_url(self):
        self.assertEqual(self.user.img_url, "/static/images/default-pic.png")

    def test_register_function(self):
        user = User.register("srh1", "sarah@gmail.com", "Sarah", "Kay", "1234567", None)
        db_user = User.query.filter_by(username='srh1').first()
        self.assertEqual(user.id, db_user.id)

    def test_authenticate_with_exist_user(self):
        user = User.authenticate("joen", "1234567")
        self.assertEqual(user.first_name, "Joene")

    def test_authenticate_with_nonexist_user(self):
        self.assertFalse(User.authenticate("hiii", "1234567"))
