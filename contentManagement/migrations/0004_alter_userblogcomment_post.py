# Generated by Django 5.0.8 on 2024-09-03 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0003_alter_userblogpost_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userblogcomment',
            name='post',
            field=models.CharField(max_length=100),
        ),
    ]
