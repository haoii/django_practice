# Generated by Django 2.1.5 on 2019-03-08 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20190306_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(verbose_name='采购日期')),
                ('clerk', models.CharField(max_length=64, verbose_name='负责人')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_num', models.IntegerField(verbose_name='序号')),
                ('quantity', models.FloatField(verbose_name='数量')),
                ('price', models.FloatField(verbose_name='单价')),
                ('is_paid', models.BooleanField(verbose_name='已付款')),
                ('remark', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Customer', verbose_name='客户')),
            ],
        ),
        migrations.AlterField(
            model_name='material',
            name='suppliers',
            field=models.ManyToManyField(through='account.MaterialSupplierRelationship', to='account.Supplier'),
        ),
        migrations.AddField(
            model_name='materialorderitem',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Material', verbose_name='材料'),
        ),
        migrations.AddField(
            model_name='materialorderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.MaterialOrder', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='materialorderitem',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Supplier', verbose_name='材料商'),
        ),
    ]
