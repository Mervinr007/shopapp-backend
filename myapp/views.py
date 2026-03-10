from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
from django.db.models import Count
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required


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
        shop=serializer.save(owner=self.request.user)
        ActivityLog.objects.create(
            user=self.request.user,
            action='shop_created',
            message=f'Added new shop "{shop.name}"'
        )
    def perform_update(self, serializer):
        shop=serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='shop_updated',
            message=f'Updated Shop "{shop.name}"'
        )
    def perform_destroy(self, instance):
        ActivityLog.objects.create(
            user=self.request.user,
            action='shop_deleted',
            message=f'Deleted Shop "{instance.name}"'
        )
        instance.delete()
        
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        product = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='product_created',
            message=f'Added new product "{product.name} ({product.weight})" to catalogue'
    )

    def perform_update(self, serializer):
        product = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='product_updated',
            message=f'Updated product "{product.name} ({product.weight})"'
    )
    
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
    def perform_create(self, serializer):
        item = serializer.save()
        ActivityLog.objects.create(
        user=self.request.user,
        action='inventory_added',
        message=f'Added "{item.product.name}" to shop "{item.shop.name}"'
    )

    def perform_update(self, serializer):
        item = serializer.save()
        ActivityLog.objects.create(
        user=self.request.user,
        action='inventory_updated',
        message=f'Updated stock for "{item.product.name}" in "{item.shop.name}"'
    )

    def perform_destroy(self, instance):
        ActivityLog.objects.create(
        user=self.request.user,
        action='inventory_removed',
        message=f'Removed "{instance.product.name}" from "{instance.shop.name}"'
    )
        instance.delete()
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
        if user.check_password(new_password):
            return Response({"error":"New password must not be the same as old password"},status=400)

        user.set_password(new_password)
        user.save()
        ActivityLog.objects.create(
            user=user,
            action='password_changed',
            message='Changed account password'
)
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
class UserPreferenceViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(preference)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_theme(self, request):
        preference, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(preference, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
class ActivityLogViewSet(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    
    @action(detail=False,methods=['get'])
    def all(self,request):
        logs=ActivityLog.objects.select_related('user').all()[:50]
        serializer=ActivityLogSerializer(logs,many=True)
        return Response(serializer.data)
    