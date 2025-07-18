# Generated by Django 5.2.4 on 2025-07-04 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_total_price'),
        ('payment', '0002_alter_payment_options_payment_checkout_request_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='merchant_request_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(default='M-Pesa', help_text='Payment method (e.g., M-Pesa)', max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(help_text='Associated order', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.order'),
        ),
    ]
