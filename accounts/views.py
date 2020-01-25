from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.api.serializers import FrnAndSugFrnSerializer
from .models import Person
from django.http import JsonResponse


class FriendsDetailAPIView(APIView):
    def post(self, request):
        data = request.data
        if 'user_name' in data:
            if Person.objects.filter(full_name=data['user_name'].lower()).exists():
                person = Person.objects.filter(full_name=data['user_name']).first()
                serializer = FrnAndSugFrnSerializer(person)
                return Response(serializer.data)
        response = JsonResponse({'error': 'no users found for given name'})
        return Response(response.content)
