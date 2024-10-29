from rest_framework import serializers
from .models import Order, OrderItem
from apps.accounts.serializers import AddressSerializer
from apps.products.serializers import ProductSerializer, ProductVariantSerializer
from apps.products.models import Product, ProductVariant
from apps.accounts.models import Address
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Generate unique order number
        while True:
            order_number = get_random_string(10).upper()
            if not Order.objects.filter(order_number=order_number).exists():
                break
                
        serializer.save(
            user=self.request.user,
            order_number=order_number
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['PENDING', 'PAID']:
            return Response(
                {"detail": "Order cannot be cancelled in current status."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'CANCELLED'
        order.save()
        return Response({"status": "Order cancelled successfully"})

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending_orders = self.get_queryset().filter(status='PENDING')
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', write_only=True, queryset=Product.objects.all()
    )
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        source='variant', write_only=True, queryset=ProductVariant.objects.all(),
        required=False, allow_null=True
    )
    total = serializers.DecimalField(
        source='get_total', read_only=True, max_digits=10, decimal_places=2
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'variant', 'variant_id', 
                 'quantity', 'price', 'total']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer(read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Address.objects.all(), source='shipping_address'
    )
    total = serializers.DecimalField(
        source='calculate_total', read_only=True, max_digits=10, decimal_places=2
    )

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'shipping_address', 
                 'shipping_address_id', 'shipping_cost', 'total_amount', 
                 'payment_method', 'items', 'total', 'created_at', 'updated_at']
        read_only_fields = ['order_number', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            # Set price from current product/variant price
            product = item_data['product']
            variant = item_data.get('variant')
            price = variant.price if variant else product.price
            
            OrderItem.objects.create(
                order=order,
                price=price,
                **item_data
            )
        
        # Calculate and update total amount
        order.total_amount = order.calculate_total()
        order.save()
        
        return order

    def validate(self, data):
        # Validate that shipping address belongs to user
        if self.context['request'].user != data['shipping_address'].user:
            raise serializers.ValidationError(
                {"shipping_address": "Invalid shipping address."}
            )
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', write_only=True, queryset=Product.objects.all()
    )
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        source='variant', write_only=True, queryset=ProductVariant.objects.all(),
        required=False, allow_null=True
    )
    total = serializers.DecimalField(
        source='get_total', read_only=True, max_digits=10, decimal_places=2
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'variant', 'variant_id', 
                 'quantity', 'price', 'total']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer(read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Address.objects.all(), source='shipping_address'
    )
    total = serializers.DecimalField(
        source='calculate_total', read_only=True, max_digits=10, decimal_places=2
    )

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'shipping_address', 
                 'shipping_address_id', 'shipping_cost', 'total_amount', 
                 'payment_method', 'items', 'total', 'created_at', 'updated_at']
        read_only_fields = ['order_number', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            # Set price from current product/variant price
            product = item_data['product']
            variant = item_data.get('variant')
            price = variant.price if variant else product.price
            
            OrderItem.objects.create(
                order=order,
                price=price,
                **item_data
            )
        
        # Calculate and update total amount
        order.total_amount = order.calculate_total()
        order.save()
        
        return order

    def validate(self, data):
        # Validate that shipping address belongs to user
        if self.context['request'].user != data['shipping_address'].user:
            raise serializers.ValidationError(
                {"shipping_address": "Invalid shipping address."}
            )
        return data
