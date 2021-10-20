import csv
from random import choice, sample
from itertools import permutations
from faker import Faker
from helpers import get_random_datetime


USERS_CSV_HEADERS = ['email', 'username', 'image_url', 'password', 'first_name', 'last_name', 'created_at']
FOLLOWS_CSV_HEADERS = ['user_being_followed_id', 'user_following_id']

NUM_USERS = 100
NUM_FOLLWERS = 1000

fake = Faker()

# Generate random profile image URLs to use for users

image_urls = [
    f"https://randomuser.me/api/portraits/{kind}/{i}.jpg"
    for kind, count in [("lego", 10), ("men", 100), ("women", 100)]
    for i in range(count)
]

with open('generator/users.csv', 'w') as users_csv:
    users_writer = csv.DictWriter(users_csv, fieldnames=USERS_CSV_HEADERS)
    users_writer.writeheader()

    for i in range(NUM_USERS):
        users_writer.writerow(dict(
            email=fake.email(),
            username=fake.user_name(),
            image_url=choice(image_urls),
            password='$2b$12$Ae6.SljpHvGGxyo5WmEte.r3zukiA0H5AeiPLEkZiH9z6fOqp.q7i',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            created_at=get_random_datetime()
        ))


# Generate follows.csv from random pairings of users

with open('generator/follows.csv', 'w') as follows_csv:
    all_pairs = list(permutations(range(1, NUM_USERS + 1), 2))

    users_writer = csv.DictWriter(follows_csv, fieldnames=FOLLOWS_CSV_HEADERS)
    users_writer.writeheader()

    for followed_user, follower in sample(all_pairs, NUM_FOLLWERS):
        users_writer.writerow(dict(user_being_followed_id=followed_user, user_following_id=follower))
