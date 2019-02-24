from django.db import models


class Customer(models.Model):
    name = models.CharField('客户名', max_length=64)
    address = models.CharField('地址', max_length=256)
    phone = models.CharField('电话', max_length=16, null=True, blank=True)

    area = models.FloatField('面积', null=True, blank=True)
    total_price = models.FloatField('总报价')

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField('材料商名', max_length=64)


