# Generated by Django 5.1.3 on 2025-01-18 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cole_buxton_be', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('footwear', 'Footwear')], default='footwear', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(default='black', max_length=100),
        ),
    ]
