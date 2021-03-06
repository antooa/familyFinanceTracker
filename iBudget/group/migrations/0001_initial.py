# Generated by Django 2.1.1 on 2018-09-19 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fund', '0001_initial'),
        ('authentication', '0001_initial'),
        ('spending', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('icon', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SharedFunds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund', models.ForeignKey(on_delete=True, to='fund.FundCategories')),
                ('group', models.ForeignKey(on_delete=True, to='group.Group')),
            ],
        ),
        migrations.CreateModel(
            name='SharedSpendingCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=True, to='group.Group')),
                ('spending_categories', models.ForeignKey(on_delete=True, to='spending.SpendingCategories')),
            ],
        ),
        migrations.CreateModel(
            name='UsersInGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField()),
                ('group', models.ForeignKey(on_delete=True, to='group.Group')),
                ('user', models.ForeignKey(on_delete=True, to='authentication.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', through='group.UsersInGroups', to='authentication.UserProfile'),
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(on_delete=False, to='authentication.UserProfile'),
        ),
        migrations.AddField(
            model_name='group',
            name='shared_funds',
            field=models.ManyToManyField(related_name='groups', through='group.SharedFunds', to='fund.FundCategories'),
        ),
        migrations.AddField(
            model_name='group',
            name='shared_spendings',
            field=models.ManyToManyField(related_name='groups', through='group.SharedSpendingCategories', to='spending.SpendingCategories'),
        ),
    ]
