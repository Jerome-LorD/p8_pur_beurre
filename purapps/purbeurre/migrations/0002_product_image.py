# Generated by Django 3.2.4 on 2021-07-04 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purbeurre', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, default=False, max_length=255),
        ),
    ]