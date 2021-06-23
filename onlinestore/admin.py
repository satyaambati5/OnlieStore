from django.contrib import admin
from .models import product ,history
# Register your models here.
# admin.site.register(product,)


class Myproduct(admin.ModelAdmin):
    model = product
    list_display = ('name','image', 'price', 'span_price', 'category',)
class myhystory(admin.ModelAdmin):
    model=history
    list_display = ('invoice_id', 'p_name', 'totalamount',
                    'purchased_time', 'customer_id', 'status', 'custmer_email')

admin.site.register(product,Myproduct)
admin.site.register(history,myhystory)
