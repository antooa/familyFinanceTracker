# Generated by Django 2.1.1 on 2018-10-09 10:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spending', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpendingLimitationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=17)),
                ('spending_category', models.ForeignKey(on_delete=True, to='spending.SpendingCategories')),
            ],
        ),
        migrations.CreateModel(
            name='SpendingLimitationIndividual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=17)),
                ('spending_category', models.ForeignKey(on_delete=True, to='spending.SpendingCategories')),
                ('user', models.ForeignKey(on_delete=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]