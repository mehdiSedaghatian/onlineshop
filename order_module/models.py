from django.db import models

from account_module.models import User
from product_module.models import Product


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    is_paid = models.BooleanField(verbose_name='is paid / is not paid')
    payment_date = models.DateField(null=True, blank=True, verbose_name='payment date')

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.count * order_detail.final_price
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.count * order_detail.product.price
        return total_amount

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return self.user.get_full_name()


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    final_price = models.IntegerField(verbose_name='final price', null=True, blank=True)
    count = models.IntegerField(verbose_name='count')

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return self.order

    class Meta:
        verbose_name = 'order detail'
        verbose_name_plural = 'order details'
