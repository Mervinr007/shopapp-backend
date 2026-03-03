from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Inventory, Shop, Product
from .serializers import *
from django.db.models import Count
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q

class GlobalSearchView(APIView):

    def get(self, request):
        query = request.GET.get('q', '').strip()

        if not query:
            return Response([])

        products = Product.objects.filter(
            Q(name__icontains=query)
        )[:5]

        shops = Shop.objects.filter(
            Q(name__icontains=query)
        )[:5]

        results = []

        for p in products:
            results.append({
                "type": "product",
                "id": p.id,
                "name": p.name,
                "weight": p.weight
            })

        for s in shops:
            results.append({
                "type": "shop",
                "id": s.id,
                "name": s.name
            })

        return Response(results)
        
        

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Shop.objects.annotate(total_products=Count('inventory'))
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Inventory.objects.select_related('product', 'shop').all()
        shop_id = self.request.query_params.get('shop')
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password incorrect"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"})

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token=request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token) 
            token.blacklist()
        except Exception as e:
            return  Response(
                {"error": "Invalid token or token already blacklisted"},
                status=status.HTTP_400_BAD_REQUEST
            )
            