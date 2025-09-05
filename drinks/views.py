from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def drink_list(request):

    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return JsonResponse({"drinks": serializer.data}, safe=False)

    if request.method == 'POST':
        data = request.data
        serializer = DrinkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# def drink_detail(request, pk):
#     try:
#         drink = Drink.objects.get(pk=pk)
#     except Drink.DoesNotExist:
#         return JsonResponse({'error': 'Drink not found'}, status=404)

#     if request.method == 'GET':
#         serializer = DrinkSerializer(drink)
#         return JsonResponse(serializer.data)

# or using decorators
@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, pk):
    try:
        drink = Drink.objects.get(pk=pk)
    except Drink.DoesNotExist:
        return Response({'error': 'Drink not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response({'message': 'Drink deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
