# Generated by Django 3.2.3 on 2021-05-29 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projecttradie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttradie',
            name='project_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='projecttradie',
            name='tradie_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
