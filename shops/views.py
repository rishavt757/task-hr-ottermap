# shops/views.py
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shop
from .serializers import ShopSerializer
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    lat_distance = math.radians(lat2 - lat1)
    lon_distance = math.radians(lon2 - lon1)
    
    a = (math.sin(lat_distance / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(lon_distance / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c  # Returns distance in kilometers

# Render the registration form
def register_shop_form(request):
    return render(request, 'shops/register.html')

# Render the search form
def search_shops_form(request):
    return render(request, 'shops/search.html')

# Shop Search API
@api_view(['GET'])
def search_shops(request):
    try:
        user_lat = float(request.query_params.get('latitude'))
        user_lon = float(request.query_params.get('longitude'))
    except (TypeError, ValueError):
        return Response({"error": "Invalid or missing latitude/longitude."}, status=status.HTTP_400_BAD_REQUEST)

    shops = Shop.objects.all()
    shop_distances = []

    for shop in shops:
        distance = haversine(user_lat, user_lon, shop.latitude, shop.longitude)
        shop_distances.append({
            "shop": ShopSerializer(shop).data,
            "distance": distance
        })

    # Sort shops based on the calculated distance
    sorted_shops = sorted(shop_distances, key=lambda x: x['distance'])

    return Response(sorted_shops)

# Registration API
@api_view(['POST'])
def register_shop(request):
    serializer = ShopSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
