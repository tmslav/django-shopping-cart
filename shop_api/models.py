from django.db import models

def hash_info(site_name,user,password):
    return str(abs(hash(site_name+user+password)))

class MemcachedKeys(models.Model):
    key = models.CharField(primary_key=True,max_length=200)
    last_used = models.DateTimeField(auto_now_add=True)

class ShopOrders(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('F', 'Failed'),
        ('D', 'Done'),
    )
    task_id = models.AutoField(primary_key=True)
    client_ip   = models.CharField(max_length=200)
    shop_name  = models.CharField(max_length=200)
    product_id = models.CharField(max_length=200)
    quantity = models.CharField(max_length=20)
    task_status = models.CharField(max_length=1,choices=STATUS)
    memcached_key = models.CharField(max_length=200)
    key = models.ForeignKey('MemcachedKeys')
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.key = MemcachedKeys.objects.get_or_create(
            key=self.memcached_key,
        )[0]
        super(ShopOrders,self).save()





