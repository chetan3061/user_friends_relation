from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FrnAndSugFrnSerializer
from .models import Person
from django.http import JsonResponse


class FriendsDetailAPIView(APIView):
    # def get(self, request, name):
    #     serializer = FrnAndSugFrnSerializer(name)
    #     return Response(serializer.data)

    def post(self, request):
        data = request.data
        if 'name' in data:
            if Person.objects.filter(full_name=data['name']).exists():
                person = Person.objects.filter(full_name=data['name']).first()
                serializer = FrnAndSugFrnSerializer(person)
                return Response(serializer.data)
        else:
            response = JsonResponse({'error': 'no users found for given name'})
            return Response(response.content)
