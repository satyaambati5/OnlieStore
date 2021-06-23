from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.db import models
import base64
import datetime
from builtins import classmethod
# Create your models here.


class product(models.Model):
   name = models.CharField(max_length=255)
   products_image = models.TextField(blank=True)
   image = models.ImageField(null=True, blank=True, upload_to='products_image')
   price = models.FloatField()
   span_price = models.FloatField()
   category = models.CharField(max_length=255)

# image processing to base64 format to manage the heroku file system
def image_to_b64(image):

    with open(image.path, "rb") as f:
        encoded_string = base64.b64encode(f.read())
        decoded_string =encoded_string.decode('utf-8')
        
        return decoded_string


@receiver(post_save, sender=product)
def create_base64_str(sender, instance=None, created=False, **kwargs):
    if created:
        instance.products_image = image_to_b64(instance.image)
        instance.image.delete()
        instance.save()
    
# # cart history model

class history(models.Model):
   invoice_id = models.CharField(max_length=500)
   p_name = models.CharField(max_length=500)
   totalamount=models.FloatField()
   purchased_time = models.DateTimeField(auto_now_add=True)
   customer_id =models.IntegerField()
   status=models.BooleanField(default=False)
   custmer_email=models.EmailField(max_length=500)

