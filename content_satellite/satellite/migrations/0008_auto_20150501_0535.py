# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0007_auto_20150331_2307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['pretty_name']},
        ),
        migrations.AddField(
            model_name='service',
            name='pretty_name',
            field=models.CharField(default='tmf_premium_service', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticker',
            name='daily_percent_change',
            field=models.DecimalField(default=0, verbose_name=b'Daily % change', max_digits=11, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticker',
            name='notes',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'Upcoming coverage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticker',
            name='scorecards_for_ticker',
            field=models.CharField(max_length=200, null=True, verbose_name=b'scorecards for ticker', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticker',
            name='tier',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='earnings_announcement',
            field=models.DateField(null=True, verbose_name=b'next earnings date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='num_followers',
            field=models.IntegerField(default=0, verbose_name=b'One followers'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticker',
            name='percent_change_historical',
            field=models.DecimalField(verbose_name=b'50D%Change', max_digits=11, decimal_places=3),
            preserve_default=True,
        ),
    ]
