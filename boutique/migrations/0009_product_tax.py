# Generated by Django 4.0.5 on 2022-10-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0008_alter_productgallery_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.FloatField(default=0.0),
        ),
    ]