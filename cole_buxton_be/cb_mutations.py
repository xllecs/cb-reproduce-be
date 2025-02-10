import graphene
from .models import CartItem
from .cb_types import CartItemType

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

class CBMutationType(graphene.ObjectType):
  add_cart_item = AddCartItem.Field()
  update_amount = UpdateAmount.Field()
  drop_cart_item = DropCartItem.Field()
