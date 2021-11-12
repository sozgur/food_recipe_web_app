from app.models import User, Category, Follows, db
from csv import DictReader
from run import app

db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

categories = ['Desserts', 'Beverages', 'Vegetables', 'Poultry', 'Beef', 'Seafood', 'Appetizers', 'Soups', 'Salads', 'Breads', 'Cakes']

for category in categories:
    db.session.add(Category(name=category))


db.session.commit()