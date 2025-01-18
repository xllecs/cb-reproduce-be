from django.db import models

# Create your models here.
class Product(models.Model):
  CATEGORIES = (
    ('footwear', 'Footwear'),
  )

  name = models.CharField(max_length=100)
  full_name = models.CharField(max_length=100, default='')
  color = models.CharField(max_length=100, default='black')
  category = models.CharField(choices=CATEGORIES, max_length=100, default='footwear')
  price = models.IntegerField(default=0)
  description = models.TextField()
  details = models.CharField(max_length=100, default='')

  class Meta:
    db_table = 'cb_product'

class ProductImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='products/')

  class Meta:
    db_table = 'cb_product_image'

class CartItem(models.Model):
  product_id = models.CharField(max_length=100)
  size = models.IntegerField(default=0)
  amount = models.IntegerField(default=1)

  class Meta:
    db_table = 'cb_cart_item'
