# Generated by Django 2.1.7 on 2019-03-15 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20190308_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=256, null=True, verbose_name='地址')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseMaterialRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='单价')),
                ('quantity', models.FloatField(verbose_name='数量')),
            ],
        ),
        migrations.AlterField(
            model_name='material',
            name='suppliers',
            field=models.ManyToManyField(through='account.MaterialSupplierRelationship', to='account.Supplier'),
        ),
        migrations.AddField(
            model_name='warehousematerialrelationship',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Material', verbose_name='材料'),
        ),
        migrations.AddField(
            model_name='warehousematerialrelationship',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Warehouse', verbose_name='仓库'),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='materials',
            field=models.ManyToManyField(through='account.WarehouseMaterialRelationship', to='account.Material'),
        ),
    ]
