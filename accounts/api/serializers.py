from .models import Person
from rest_framework import serializers
from django.db.models import Count


class FrnAndSugFrnSerializer(serializers.Serializer):
    PersonFriendsRelation = Person.friends.through
    friends = serializers.SerializerMethodField()
    suggested_friends = serializers.SerializerMethodField()

    def get_friends(self, person):
        friends_list = person.friends.values_list('full_name', flat=True)
        print(len(friends_list))
        return list(friends_list)

    def get_suggested_friends(self, person):
        friends_ids = person.friends.values_list('id', flat=True)
        suggested_friends = Person.objects.filter(friends__in=friends_ids).\
            exclude(id__in=friends_ids).\
            exclude(id=person.id).\
            values_list('full_name', flat=True).\
            annotate(count=Count('full_name')).order_by('count')
        print(len(suggested_friends))
        return list(suggested_friends)
