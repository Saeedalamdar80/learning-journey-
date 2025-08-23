from django.db import models
from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField() 
    # product_user
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True,
                                         related_name='+')

class Product(models.Model):
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    inventory = models.IntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZ = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_STATUS = [
        (MEMBERSHIP_BRONZ, 'Bronz'),
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField(auto_now=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_STATUS, default=MEMBERSHIP_BRONZ)
    class Meta:
        pass

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS = [
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
        (PAYMENT_PENDING, 'Pending')
    ]
    placed_at = models.DateTimeField(auto_created=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

