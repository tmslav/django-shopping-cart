from django.db import models


class ShopOrders(models.Model):
    SHIRT_SIZES = (
        ('P', 'Pending'),
        ('F', 'Failed'),
        ('D', 'Done'),
    )
    shop_name  = models.CharField(max_length=200)
    user_name  = models.CharField(max_length=200)
    password   = models.CharField(max_length=200)
    product_id = models.CharField(max_length=200)
    task_status = models.CharField(max_length=1,choices=SHIRT_SIZES)
    task_id = models.CharField(max_length=50)

