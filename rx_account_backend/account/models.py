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
        return self.name


class CollectionFromCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    amount = models.FloatField('金额')
    collect_date = models.DateField('收款日期')
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.customer) + '_' + str(self.amount) + '元'


class MaterialFirstClass(models.Model):
    name = models.CharField('类别名称', max_length=64)
    description = models.CharField('描述', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name


class MaterialSecondClass(models.Model):
    name = models.CharField('类别名称', max_length=64)
    first_class = models.ForeignKey(MaterialFirstClass, on_delete=models.CASCADE, verbose_name='一级类别')
    description = models.CharField('描述', max_length=256, null=True, blank=True)

    def __str__(self):
        return str(self.first_class) + '_' + self.name


class MaterialThirdClass(models.Model):
    name = models.CharField('类别名称', max_length=64)
    second_class = models.ForeignKey(MaterialSecondClass, on_delete=models.CASCADE, verbose_name='二级类别')
    description = models.CharField('描述', max_length=256, null=True, blank=True)

    def __str__(self):
        return str(self.second_class) + '_' + self.name


class Material(models.Model):
    name = models.CharField('材料名称', max_length=64)
    material_class = models.ForeignKey(MaterialThirdClass, on_delete=models.CASCADE, verbose_name='类别')
    unit = models.CharField('单位', max_length=16)
    description = models.CharField('描述', max_length=256, null=True, blank=True)
    suppliers = models.ManyToManyField(Supplier, through='MaterialSupplierRelationship')

    total_used_amount = models.FloatField('总用量', null=True, blank=True)
    total_expense = models.FloatField('总花费', null=True, blank=True)

    def __str__(self):
        return self.name


class MaterialSupplierRelationship(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='材料商')
    price = models.FloatField('单价')

    def __str__(self):
        return str(self.material) + ' - 与 - ' + str(self.supplier)


class Warehouse(models.Model):
    name = models.CharField('仓库名', max_length=64)
    address = models.CharField('地址', max_length=256, null=True, blank=True)
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    materials = models.ManyToManyField(Material, through='WarehouseMaterialRelationship')

    def __str__(self):
        return self.name+'(仓库)'


class WarehouseMaterialRelationship(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='仓库')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')
    price = models.FloatField('单价')
    quantity = models.FloatField('数量')

    def __str__(self):
        return str(self.warehouse) + ' - 与 - ' + str(self.material)


class MaterialOrder(models.Model):
    order_date = models.DateField('采购日期')
    clerk = models.CharField('负责人', max_length=64)
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    customers = models.ManyToManyField(Customer, through='CustomerInOrderRelationship')
    materials = models.ManyToManyField(Material, through='MaterialInOrderRelationship')
    warehouses = models.ManyToManyField(Warehouse, through='WarehouseInOrderRelationship')
    suppliers = models.ManyToManyField(Supplier, through='SupplierInOrderRelationship')

    def __str__(self):
        return '订单号：' + str(self.id)


class MaterialInOrderRelationship(models.Model):
    order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE, verbose_name='订单')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')

    quantity = models.FloatField('总数量')
    expense = models.FloatField('总花费')
    paid_ratio = models.FloatField('已支付比例')

    warehouses = models.ManyToManyField(Warehouse, through='WarehouseInMaterialInOrderRelationship')
    suppliers = models.ManyToManyField(Supplier, through='SupplierInMaterialInOrderRelationship')

    def __str__(self):
        return str(self.order) + ' - 与 - ' + str(self.material)


class WarehouseInMaterialInOrderRelationship(models.Model):
    material_in_order = models.ForeignKey(MaterialInOrderRelationship, on_delete=models.CASCADE, verbose_name='订单材料')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='仓库')
    quantity = models.FloatField('数量')
    price = models.FloatField('单价')
    is_paid = models.BooleanField('已支付', default=True)
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.material_in_order) + ' - 与 - ' + str(self.warehouse)


class SupplierInMaterialInOrderRelationship(models.Model):
    material_in_order = models.ForeignKey(MaterialInOrderRelationship, on_delete=models.CASCADE, verbose_name='订单材料')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='材料商')
    quantity = models.FloatField('数量')
    price = models.FloatField('单价')
    is_paid = models.BooleanField('已支付')
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.material_in_order) + ' - 与 - ' + str(self.supplier)


class CustomerInOrderRelationship(models.Model):
    order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE, verbose_name='订单')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')

    materials = models.ManyToManyField(Material, through='MaterialInCustomerInOrderRelationship')

    def __str__(self):
        return str(self.order) + ' - 与 - ' + str(self.customer)


class MaterialInCustomerInOrderRelationship(models.Model):
    customer_in_order = models.ForeignKey(CustomerInOrderRelationship, on_delete=models.CASCADE, verbose_name='订单客户')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')
    quantity = models.FloatField('数量')
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    material_in_order = models.ForeignKey(MaterialInOrderRelationship, on_delete=models.CASCADE, verbose_name='订单材料')

    def __str__(self):
        return str(self.customer_in_order) + ' - 与 - ' + str(self.material)


class WarehouseInOrderRelationship(models.Model):
    order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE, verbose_name='订单')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='仓库')

    is_paid = models.BooleanField('已支付', default=True)
    expense = models.FloatField('总花费')

    materials = models.ManyToManyField(Material, through='MaterialInWarehouseInOrderRelationship')

    def __str__(self):
        return str(self.order) + ' - 与 - ' + str(self.warehouse)


class SupplierInOrderRelationship(models.Model):
    order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE, verbose_name='订单')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='材料商')

    is_paid = models.BooleanField('已支付')
    expense = models.FloatField('总花费')

    materials = models.ManyToManyField(Material, through='MaterialInSupplierInOrderRelationship')

    def __str__(self):
        return str(self.order) + ' - 与 - ' + str(self.supplier)


class MaterialInWarehouseInOrderRelationship(models.Model):
    warehouse_in_order = models.ForeignKey(WarehouseInOrderRelationship, on_delete=models.CASCADE, verbose_name='订单仓库')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')
    quantity = models.FloatField('数量')
    price = models.FloatField('单价')
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.warehouse_in_order) + ' - 与 - ' + str(self.material)


class MaterialInSupplierInOrderRelationship(models.Model):
    supplier_in_order = models.ForeignKey(SupplierInOrderRelationship, on_delete=models.CASCADE, verbose_name='订单材料商')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')
    quantity = models.FloatField('数量')
    price = models.FloatField('单价')
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.supplier_in_order) + ' - 与 - ' + str(self.material)



class MaterialOrderDemandItem(models.Model):
    order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE, verbose_name='订单')
    item_num = models.IntegerField('序号')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    quantity = models.FloatField('数量')

    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.order) + ' - ' + str(self.item_num) + ' - ' + str(self.material) + ' - ' + str(self.customer)


class MaterialOrderPurchaseItem(models.Model):
    PURCHASE_TYPE = (
        ('W', 'Warehouse'),
        ('S', 'Supplier'),
    )

    order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE, verbose_name='订单')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='材料')
    purchase_type = models.CharField(max_length=1, choices=PURCHASE_TYPE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='仓库', null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='材料商', null=True, blank=True)
    quantity = models.FloatField('数量')
    price = models.FloatField('单价')
    is_paid = models.BooleanField('已支付')
    remark = models.CharField('备注', max_length=512, null=True, blank=True)

    def __str__(self):
        if str(self.purchase_type) == 'W':
            return str(self.order) + ' - ' + str(self.material) + ' - ' + str(self.warehouse)
        else:
            return str(self.order) + ' - ' + str(self.material) + ' - ' + str(self.supplier)






