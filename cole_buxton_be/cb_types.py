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
  product = graphene.Field(ProductType, id=graphene.ID(), full_name=graphene.String())
  products = graphene.List(ProductType, collection=graphene.String())
  images = graphene.List(ProductImageType, product_code=graphene.String(required=True))
  product_images = graphene.List(ProductImageType, product_id=graphene.ID())
  product_sizes = graphene.List(ProductSizeType, product_id=graphene.ID(required=True))
  cart_items = graphene.List(CartItemType)

  def resolve_product(self, info, id=None, full_name=None):
    cache_key = f"product:{id or full_name}"

    # redis_client.delete(cache_key)
    cached_product = redis_client.hgetall(cache_key)
    # print(cached_product)
    if cached_product:
      product_type = ProductType(id=cached_product['id'], name=cached_product['name'], color=cached_product['color'], price=cached_product['price'], description=cached_product['description'], details=cached_product['details'])
      product_type.pk = cached_product['id']
      return product_type
    
    if id:
      product = Product.objects.get(id=id)
      redis_client.hset(cache_key, mapping={ 'id': id, 'name': product.name, 'color': product.color, 'price': product.price, 'description': product.description, 'details': product.details })
      redis_client.expire(cache_key, 3600)
      return product

    if full_name:
      product = Product.objects.get(full_name=full_name)
      redis_client.hset(cache_key, mapping={ 'id': full_name, 'name': product.name, 'color': product.color, 'price': product.price, 'description': product.description, 'details': product.details })
      redis_client.expire(cache_key, 3600)
      return product
    
    return None

  def resolve_products(self, info, collection=None):
    if collection:
      return Product.objects.filter(collection=collection)

    return Product.objects.all()
  
  def resolve_images(self, info, product_code):
    return ProductImage.objects.filter(product_code=product_code)
	
  def resolve_product_images(self, info, product_id):
    return ProductImage.objects.filter(product_id=product_id)
  
  def resolve_product_sizes(self, info, product_id):
    if product_id.isdigit():
      product = Product.objects.get(id=product_id)
    else:
      product = Product.objects.get(full_name=product_id)
    return product.sizes.all()

  def resolve_cart_items(self, info):
    return CartItem.objects.all()
