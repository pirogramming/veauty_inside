# Generated by Django 2.2.4 on 2019-08-13 03:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0005_auto_20190809_0022'),
        ('accounts', '0005_auto_20190812_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='my_cosmetic',
            field=models.ManyToManyField(related_name='my_cosmetics', to='beauty.Cosmetic'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.DateField(default=datetime.datetime(2019, 8, 13, 3, 30, 50, 39384, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='cosmetic',
            field=models.ManyToManyField(related_name='cosmetics', to='beauty.Cosmetic'),
        ),
    ]