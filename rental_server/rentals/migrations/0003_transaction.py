# Generated by Django 2.2.5 on 2020-03-15 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_rental_expired'),
    ]

    operations = [
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.FloatField()),
                ('transaction_time', models.DateField(auto_now=True)),
                ('charge_id', models.TextField()),
                ('refund_status', models.BooleanField()),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='rentals.rental')),
            ],
        ),
    ]
