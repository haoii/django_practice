# Generated by Django 2.1.7 on 2019-03-19 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_auto_20190315_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Customer', verbose_name='客户')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialInCustomerInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='数量')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
                ('customer_in_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.CustomerInOrderRelationship', verbose_name='订单客户')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='总数量')),
                ('expense', models.FloatField(verbose_name='总花费')),
                ('paid_ratio', models.FloatField(verbose_name='已支付比例')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialInSupplierInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='数量')),
                ('price', models.FloatField(verbose_name='单价')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialInWarehouseInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='数量')),
                ('price', models.FloatField(verbose_name='单价')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierInMaterialInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='数量')),
                ('price', models.FloatField(verbose_name='单价')),
                ('is_paid', models.BooleanField(verbose_name='已支付')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
                ('material_in_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialInOrderRelationship', verbose_name='订单材料')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Supplier', verbose_name='材料商')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(verbose_name='已支付')),
                ('expense', models.FloatField(verbose_name='总花费')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseInMaterialInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='数量')),
                ('price', models.FloatField(verbose_name='单价')),
                ('is_paid', models.BooleanField(default=True, verbose_name='已支付')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
                ('material_in_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialInOrderRelationship', verbose_name='订单材料')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Warehouse', verbose_name='仓库')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseInOrderRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=True, verbose_name='已支付')),
            ],
        ),
        migrations.AlterField(
            model_name='material',
            name='suppliers',
            field=models.ManyToManyField(through='account.MaterialSupplierRelationship', to='account.Supplier'),
        ),
        migrations.AddField(
            model_name='warehouseinorderrelationship',
            name='materials',
            field=models.ManyToManyField(through='account.MaterialInWarehouseInOrderRelationship', to='account.Material'),
        ),
        migrations.AddField(
            model_name='warehouseinorderrelationship',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialOrder', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='warehouseinorderrelationship',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Warehouse', verbose_name='仓库'),
        ),
        migrations.AddField(
            model_name='supplierinorderrelationship',
            name='materials',
            field=models.ManyToManyField(through='account.MaterialInSupplierInOrderRelationship', to='account.Material'),
        ),
        migrations.AddField(
            model_name='supplierinorderrelationship',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialOrder', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='supplierinorderrelationship',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Supplier', verbose_name='材料商'),
        ),
        migrations.AddField(
            model_name='materialinwarehouseinorderrelationship',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Material', verbose_name='材料'),
        ),
        migrations.AddField(
            model_name='materialinwarehouseinorderrelationship',
            name='warehouse_in_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.WarehouseInOrderRelationship', verbose_name='订单仓库'),
        ),
        migrations.AddField(
            model_name='materialinsupplierinorderrelationship',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Material', verbose_name='材料'),
        ),
        migrations.AddField(
            model_name='materialinsupplierinorderrelationship',
            name='supplier_in_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.SupplierInOrderRelationship', verbose_name='订单材料商'),
        ),
        migrations.AddField(
            model_name='materialinorderrelationship',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Material', verbose_name='材料'),
        ),
        migrations.AddField(
            model_name='materialinorderrelationship',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialOrder', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='materialinorderrelationship',
            name='suppliers',
            field=models.ManyToManyField(through='account.SupplierInMaterialInOrderRelationship', to='account.Supplier'),
        ),
        migrations.AddField(
            model_name='materialinorderrelationship',
            name='warehouses',
            field=models.ManyToManyField(through='account.WarehouseInMaterialInOrderRelationship', to='account.Warehouse'),
        ),
        migrations.AddField(
            model_name='materialincustomerinorderrelationship',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Material', verbose_name='材料'),
        ),
        migrations.AddField(
            model_name='materialincustomerinorderrelationship',
            name='material_in_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialInOrderRelationship', verbose_name='订单材料'),
        ),
        migrations.AddField(
            model_name='customerinorderrelationship',
            name='materials',
            field=models.ManyToManyField(through='account.MaterialInCustomerInOrderRelationship', to='account.Material'),
        ),
        migrations.AddField(
            model_name='customerinorderrelationship',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialOrder', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='materialorder',
            name='customers',
            field=models.ManyToManyField(through='account.CustomerInOrderRelationship', to='account.Customer'),
        ),
        migrations.AddField(
            model_name='materialorder',
            name='materials',
            field=models.ManyToManyField(through='account.MaterialInOrderRelationship', to='account.Material'),
        ),
        migrations.AddField(
            model_name='materialorder',
            name='suppliers',
            field=models.ManyToManyField(through='account.SupplierInOrderRelationship', to='account.Supplier'),
        ),
        migrations.AddField(
            model_name='materialorder',
            name='warehouses',
            field=models.ManyToManyField(through='account.WarehouseInOrderRelationship', to='account.Warehouse'),
        ),
    ]
