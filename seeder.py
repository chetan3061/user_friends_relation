import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_friends_relation.settings')
import django
django.setup()
from faker import Faker
from accounts.models import Person
import random
fake = Faker()

Person.objects.all().delete()


def custom_random_int(from_id, to_id, exclude_id):
    random_int = random.randint(from_id, to_id)
    if random_int not in exclude_id:
        return random_int
    else:
        return custom_random_int(from_id, to_id, exclude_id)


class SeedFakeData(object):
    PersonFriendsRelation = Person.friends.through

    def __init__(self, total_size, bulk_size=100):
        if bulk_size < 50:
            print('bulk_size should be greater than 50')
        self.bulk_size = bulk_size
        self.total_size = total_size
        self.objects_list = []
        self.count = 0
        self.relation = []

    def commit(self):
        Person.objects.bulk_create(self.objects_list)
        self.objects_list = []

    def seed_persons_to_database(self):
        for _ in range(self.total_size):
            full_name = fake.name()
            self.objects_list.append(Person(full_name=full_name))
            self.count += 1
            percent_complete = self.count / self.total_size * 100
            print(
                "Adding {} new Users to database: {:.2f}%".format(self.total_size, percent_complete),
                end='\r',
                flush=True
            )
            if len(self.objects_list) >= self.bulk_size:
                self.commit()

    def complete_commit(self):
        if len(self.objects_list) > 0:
            self.commit()
        self.count = 0

    def build_reverse_relation_for_friends(self):
        self.count = 0
        last_person_seeded_id = Person.objects.all().last().id
        for to_person_id in range(last_person_seeded_id - self.total_size + 1, last_person_seeded_id):
            self.count += 1
            from_person_ids = self.PersonFriendsRelation.objects.all().filter(from_person_id=to_person_id).\
                values_list('to_person_id', flat=True)
            for from_person_id in from_person_ids:
                self.relation.append(
                    self.PersonFriendsRelation(from_person_id=from_person_id, to_person_id=to_person_id)
                )
            if len(self.relation) > self.bulk_size*30:
                self.add_m2m_relation_table_to_data(ignore_conflicts=True)
            percent_complete = (self.count+1) / self.total_size * 100
            print(
                "Adding reverse_relation_table to database: {:.2f}%".format(percent_complete),
                end='\r',
                flush=True
            )
        if len(self.relation) >= 0:
            self.add_m2m_relation_table_to_data(ignore_conflicts=True)

    def add_m2m_relation_table_to_data(self, ignore_conflicts=False):
        self.PersonFriendsRelation.objects.bulk_create(self.relation, ignore_conflicts=ignore_conflicts)
        self.relation = []

    def create_m2m_relation_table(self):
        last_person_seeded_id = Person.objects.all().last().id
        self.count = 0
        for from_person_id in range(last_person_seeded_id-self.total_size+1, last_person_seeded_id):
            exclude_id = []
            for _ in range(50):
                friend_id = custom_random_int(last_person_seeded_id-self.total_size+1, last_person_seeded_id, exclude_id)
                exclude_id.append(friend_id)
                self.count += 1
                self.relation.append(self.PersonFriendsRelation(from_person_id=from_person_id, to_person_id=friend_id))
                percent_complete = (self.count+50) / (self.total_size*50) * 100
                print(
                    "Adding relation_table to database: {:.2f}%".format(percent_complete),
                    end='\r',
                    flush=True
                )
                if len(self.relation) >= self.bulk_size*50:
                    self.add_m2m_relation_table_to_data()
        if len(self.relation) >= 0:
            self.add_m2m_relation_table_to_data()

    def run(self):
        self.count = 0
        self.seed_persons_to_database()
        self.complete_commit()
        print('\n creating relation table')
        self.create_m2m_relation_table()
        print('\n now adding reverse relationship to database')
        self.build_reverse_relation_for_friends()
        print('\n database update completed')
        self.count = 0
        self.relation = []


def create_database(data_size=1000):
    fake_data_seeder = SeedFakeData(data_size)
    fake_data_seeder.run()


create_database()
