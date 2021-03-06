# Generated by Django 2.1.5 on 2019-03-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20190305_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='total_expense',
            field=models.FloatField(blank=True, null=True, verbose_name='总花费'),
        ),
        migrations.AddField(
            model_name='material',
            name='total_used_amount',
            field=models.FloatField(blank=True, null=True, verbose_name='总用量'),
        ),
        migrations.AlterField(
            model_name='material',
            name='suppliers',
            field=models.ManyToManyField(through='account.MaterialSupplierRelationship', to='account.Supplier'),
        ),
    ]
