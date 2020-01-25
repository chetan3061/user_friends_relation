from rest_framework.test import APITestCase
from accounts.models import Person
from rest_framework.reverse import reverse
from rest_framework import status


class PersonAPITestCase(APITestCase):
    def setUp(self):
        chetan = Person.objects.create(full_name='chetan')
        siddhu = Person.objects.create(full_name='siddhu')
        mouli = Person.objects.create(full_name='mouli')
        ram = Person.objects.create(full_name='ram')
        ravi = Person.objects.create(full_name='ravi')
        nihit = Person.objects.create(full_name='nihit')
        shiva = Person.objects.create(full_name='shiva')
        shiva.friends.add(chetan)
        nihit.friends.add(mouli, siddhu, chetan)
        mouli.friends.add(chetan, siddhu, ravi, ram)
        siddhu.friends.add(chetan, ravi)
        chetan.friends.add(ravi, ram)

    def test_person_friends_suggested_friends(self):
        data = {"user_name":"nihit"}
        url = reverse("person:friends_list")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'friends': ['chetan', 'siddhu', 'mouli'], 'suggested_friends': ['ravi', 'ram', 'shiva']}
                         )