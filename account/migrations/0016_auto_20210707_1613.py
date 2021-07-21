# Generated by Django 3.2.5 on 2021-07-07 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20210707_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='Account number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='card_number',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='Card number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id_number',
            field=models.CharField(max_length=10, null=True, unique=True, verbose_name='ID card number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='meli',
            field=models.CharField(max_length=10, null=True, unique=True, verbose_name='National ID number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='shaba_number',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='Shaba number'),
        ),
    ]
