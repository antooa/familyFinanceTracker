# Generated by Django 2.1.1 on 2018-10-03 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20180921_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_sys_admin',
            field=models.BooleanField(default=False),
        ),
    ]
