# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0006_auto_20150312_0031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date_pub']},
        ),
        migrations.AlterModelOptions(
            name='scorecard',
            options={'ordering': ['pretty_name']},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='servicetake',
            options={'ordering': ['scorecard']},
        ),
        migrations.AlterModelOptions(
            name='ticker',
            options={'ordering': ['ticker_symbol']},
        ),
        migrations.AlterField(
            model_name='ticker',
            name='company_name',
            field=models.CharField(max_length=120, null=True, verbose_name=b'name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='earnings_announcement',
            field=models.DateField(null=True, verbose_name=b'earnings date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='exchange_symbol',
            field=models.CharField(max_length=10, verbose_name=b'exchange'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='num_followers',
            field=models.IntegerField(default=0, verbose_name=b'followers'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='percent_change_historical',
            field=models.DecimalField(verbose_name=b'% change 50d', max_digits=11, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='ticker_symbol',
            field=models.CharField(max_length=5, verbose_name=b'symbol'),
            preserve_default=True,
        ),
    ]
