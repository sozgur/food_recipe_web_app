from app import create_app
app = create_app()

from unittest import TestCase

class CategoryTestCase(TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_recipe_list(self):
        with self.client:
            res = self.client.get("/categories/1/recipes")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 class="mt-4">Recipes</h3>', html)