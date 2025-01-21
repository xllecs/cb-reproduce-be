import graphene
from graphene_django import DjangoObjectType
from cole_buxton_be.models import Product, ProductImage, ProductSize, CartItem

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

class Query(graphene.ObjectType):
  product = graphene.Field(ProductType, id=graphene.ID(), full_name=graphene.String())
  products = graphene.List(ProductType, category=graphene.String())
  product_images = graphene.List(ProductImageType, product_id=graphene.ID())
  product_sizes = graphene.List(ProductSizeType, product_id=graphene.ID(required=True))
  cart_items = graphene.List(CartItemType)

  def resolve_product(self, info, id=None, full_name=None):
    if id:  
      return Product.objects.get(id=id)

    if full_name:
      return Product.objects.get(full_name=full_name)
    
    return None

  def resolve_products(self, info, category=None):
    if category:
      return Product.objects.filter(category=category)

    return Product.objects.all()
	
  def resolve_product_images(self, info, product_id):
    return ProductImage.objects.filter(product_id=product_id)
  
  def resolve_product_sizes(self, info, product_id):
    product = Product.objects.get(id=product_id)
    return product.sizes.all() 

  def resolve_cart_items(self, info):
    return CartItem.objects.all()
  
class AddCartItem(graphene.Mutation):
  class Arguments:
    product_id = graphene.ID(required=True)
    size = graphene.String(required=True)

  ok = graphene.Boolean()
  cart_item = graphene.Field(lambda: CartItemType)

  def mutate(root, info, product_id, size):
    if (CartItem.objects.filter(product_id=product_id, size=size).exists()):
      cart_item = CartItem.objects.get(product_id=product_id, size=size)
      cart_item.amount += 1
      cart_item.save()
      ok = True
    else:
      cart_item = CartItem(product_id=product_id, size=size)
      cart_item.save()
      ok = True

    return AddCartItem(cart_item=cart_item, ok=ok)
  
class UpdateAmount(graphene.Mutation):
  class Arguments:
    cart_item_id = graphene.ID(required=True)
    increase = graphene.Boolean(required=True)

  cart_item = graphene.Field(lambda: CartItemType)
  
  def mutate(root, info, cart_item_id, increase):
    cart_item = CartItem.objects.get(id=cart_item_id)

    if increase:
      cart_item.amount += 1
      cart_item.save()
    else:
      if cart_item.amount > 1:
        cart_item.amount -= 1
        cart_item.save()

    return UpdateAmount(cart_item=cart_item)

class DropCartItem(graphene.Mutation):
  class Arguments:
    cart_item_id = graphene.ID(required=True)

  ok = graphene.Boolean()

  def mutate(root, info, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    ok = True

    return DropCartItem(ok=ok)

class Mutation(graphene.ObjectType):
  add_cart_item = AddCartItem.Field()
  update_amount = UpdateAmount.Field()
  drop_cart_item = DropCartItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
