# Generated by Django 5.0.8 on 2024-09-04 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0004_alter_userblogcomment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userblogcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='contentManagement.userblogpost'),
        ),
    ]
