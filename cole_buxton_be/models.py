from django.db import models

# Create your models here.
class Product(models.Model):
  COLLECTIONS = (
    ('new-launches', 'New Launches'),
    ('anniversary-drop', 'Anniversary Drop'),
    ('footwear', 'Footwear'),
  )

  name = models.CharField(max_length=100)
  code = models.CharField(max_length=100, default='')
  color = models.CharField(max_length=100, default='black')
  collection = models.CharField(choices=COLLECTIONS, max_length=100, default='footwear')
  price = models.IntegerField(default=0)
  description = models.TextField()
  details = models.CharField(max_length=100, default='')

  def __str__(self):
    return self.code

  class Meta:
    db_table = 'cb_product'

class ProductImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
  url = models.ImageField(upload_to='products/')

  def __str__(self):
    return self.product.code

  class Meta:
    db_table = 'cb_product_image'

class ProductSize(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
  letter = models.CharField(max_length=5)
  stock = models.IntegerField()

  def __str__(self):
    return self.product.code + '-' + self.letter

  class Meta:
    db_table = 'cb_product_size'

class CartItem(models.Model):
  product_code = models.CharField(max_length=100)
  size = models.CharField(default='', max_length=5)
  amount = models.IntegerField(default=1)

  class Meta:
    db_table = 'cb_cart_item'
