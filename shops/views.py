from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from shops.models import Shop
from .serializers import ShopSerializer
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    lat_distance = math.radians(lat2 - lat1)
    lon_distance = math.radians(lon2 - lon1)
    
    a = (math.sin(lat_distance / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(lon_distance / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


@api_view(['GET'])
def search_shops(request):
    try:
        user_lat = float(request.GET.get('latitude'))
        user_lon = float(request.GET.get('longitude'))
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

    sorted_shops = sorted(shop_distances, key=lambda x: x['distance'])

    return render(request, 'shops/search.html', {'distances': sorted_shops})


def register_shop_form(request, success_message=None):
    return render(request, 'shops/register.html', {'success_message': success_message})


def search_shops_form(request):
    return render(request, 'shops/search.html')


@api_view(['POST'])
def register_shop(request):
    serializer = ShopSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return register_shop_form(request, success_message='Registration successful!')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    shop.delete()
    return Response({"message": "Shop deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def view_all_shops(request):
    shops = Shop.objects.all()
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
