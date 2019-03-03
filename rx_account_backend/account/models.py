from django.db import models


class Customer(models.Model):
    name = models.CharField('客户名', max_length=64)
    address = models.CharField('地址', max_length=256, primary_key=True)
    sign_date = models.DateField('签单日期')
    duration = models.IntegerField('工期')
    phone = models.CharField('电话', max_length=16, null=True, blank=True)

    area = models.FloatField('面积', null=True, blank=True)
    total_price = models.FloatField('总报价')
    price_discount = models.FloatField('折扣')
    price_received = models.FloatField('报价已到账', null=True, blank=True)
    total_expense = models.FloatField('总开销', null=True, blank=True)
    expense_paid = models.FloatField('开销已出账', null=True, blank=True)

    def __str__(self):
        return self.name + '(' + self.address + ')'


class Supplier(models.Model):
    name = models.CharField('材料商名', max_length=64)
    address = models.CharField('地址', max_length=256, null=True, blank=True)
    phone = models.CharField('电话', max_length=16, null=True, blank=True)

    total_expense = models.FloatField('总材料费', null=True, blank=True)
    expense_paid = models.FloatField('总材料费已支付', null=True, blank=True)

    def __str__(self):
        return self.name + '(' + str(self.id) + ' )'


class CollectionFromCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField('金额')
    collect_date = models.DateField('收款日期')
    remark = models.CharField('备注', max_length=512)

    def __str__(self):
        return str(self.customer) + ' - ' + str(self.amount) + '元'




