# Generated by Django 3.2.4 on 2021-07-31 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre', '0007_auto_20210726_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='nutriments',
            field=models.CharField(blank=True, default=False, max_length=150),
        ),
    ]
