# Generated by Django 2.2.5 on 2020-02-26 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0002_auto_20200226_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rented_server',
            name='secondary_id',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='unrented_server',
            name='secondary_id',
            field=models.TextField(),
        ),
    ]
