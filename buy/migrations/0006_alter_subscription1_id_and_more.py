# Generated by Django 5.0.2 on 2024-04-26 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy', '0005_alter_subscription1_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription1',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='subscription2',
            name='subcribe_price',
            field=models.IntegerField(default=99),
        ),
        migrations.AlterField(
            model_name='subscription3',
            name='subcribe_price',
            field=models.IntegerField(default=149),
        ),
    ]