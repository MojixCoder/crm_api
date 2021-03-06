# Generated by Django 3.2.5 on 2021-07-06 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birth date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at'),
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
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at'),
        ),
    ]
