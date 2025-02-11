from .models import Product, ProductImage, ProductSize, CartItem
from graphene_django import DjangoObjectType
import graphene

import redis
from django.core.cache import cache

redis_client = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)

class ProductType(DjangoObjectType):
	class Meta:
		model = Product
		fields = '__all__'

class ProductImageType(DjangoObjectType):
	class Meta:
		model = ProductImage
		fields = '__all__'
      
class ProductSizeType(DjangoObjectType):
  class Meta:
    model = ProductSize
    fields = '__all__'

class CartItemType(DjangoObjectType):
  class Meta:
    model = CartItem
    fields = '__all__'

class CBQueryType(graphene.ObjectType):
  product = graphene.Field(ProductType, code=graphene.String())
  products = graphene.List(ProductType, collection=graphene.String(), name=graphene.String())
  product_images = graphene.List(ProductImageType, product_id=graphene.ID(), product_code=graphene.String())
  product_sizes = graphene.List(ProductSizeType, product_code=graphene.String(required=True))
  cart_items = graphene.List(CartItemType)

  # def resolve_product(self, info, id=None, full_name=None):
  def resolve_product(self, info, code=None):
    cache_key = f"product:{code}"

    cached_product = redis_client.hgetall(cache_key)

    redis_client.delete(cache_key)
    # if cached_product:
    #   product_type = ProductType(id=cached_product['id'], product_code=cached_product['code'], name=cached_product['name'], color=cached_product['color'], price=cached_product['price'], description=cached_product['description'], details=cached_product['details'])
    #   product_type.pk = cached_product['id']
    #   return product_type

    product = Product.objects.get(code=code)
    redis_client.hset(cache_key, mapping={ 'id': product.id, 'code': code, 'name': product.name, 'color': product.color, 'price': product.price, 'description': product.description, 'details': product.details })
    redis_client.expire(cache_key, 3600)

    return product

  def resolve_products(self, info, collection=None, name=None):
    if collection:
      return Product.objects.filter(collection=collection)

    if name:
      return Product.objects.filter(name=name)

    return Product.objects.all()
	
  def resolve_product_images(self, info, product_id=None, product_code=None):
    # if product_id:
    #   return ProductImage.objects.filter(product_id=product_id)

    if product_code:
      return ProductImage.objects.filter(product__code=product_code)
  
  def resolve_product_sizes(self, info, product_code):
    # if product_id.isdigit():
    #   product = Product.objects.get(id=product_id)
    # else:
    product = Product.objects.get(code=product_code)
    return product.sizes.all()

  def resolve_cart_items(self, info):
    return CartItem.objects.all()
