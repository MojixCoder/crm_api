# Generated by Django 3.2.5 on 2021-07-06 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20210706_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birth date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='end_work',
            field=models.DateField(blank=True, null=True, verbose_name='End of work date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='start_work',
            field=models.DateField(blank=True, null=True, verbose_name='Start of work date'),
        ),
    ]
