# Generated by Django 3.1.5 on 2021-04-29 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0006_hospital_non_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='Ratings_stars',
            field=models.CharField(blank=True, default='', max_length=5),
        ),
    ]
