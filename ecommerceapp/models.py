from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    description=models.TextField(max_length=500)
    number=models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=60,default="")
    subcategory = models.CharField(max_length=60,default="")
    price = models.CharField(max_length=50,default="0")
    desc = models.CharField(max_length=250)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.product_name
    
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=6000)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50,default="")
    amount =models.IntegerField(default=0)
    mobile_no = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)

    paymentstatus = models.CharField(max_length=20,blank=True,default="UNPAID")


    def __str__(self):
        return self.fname
    
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=100,default="")
    update_desc = models.CharField(max_length=5000)
    deliverd = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7]+" ..."
    