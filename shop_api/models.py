from django.db import models


class ShopOrders(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('F', 'Failed'),
        ('D', 'Done'),
    )
    task_id = models.AutoField(primary_key=True)
    shop_name  = models.CharField(max_length=200)
    user_name  = models.CharField(max_length=200)
    password   = models.CharField(max_length=200)
    product_id = models.CharField(max_length=200)
    quantity = models.CharField(max_length=20)
    task_status = models.CharField(max_length=1,choices=STATUS)

