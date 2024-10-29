from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children']
        read_only_fields = ['slug']

    def get_children(self, obj):
        return CategorySerializer(obj.category_set.all(), many=True).data

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']

class ProductVariantSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'value', 'price_adjustment', 'stock_quantity', 'price']

    def get_price(self, obj):
        return obj.product.price + obj.price_adjustment

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'slug', 'category', 'category_id',
                 'description', 'price', 'stock_quantity', 'weight',
                 'is_active', 'created_at', 'updated_at', 'images',
                 'variants', 'primary_image']
        read_only_fields = ['sku', 'slug', 'created_at', 'updated_at']

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None
