# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0031_auto_20150730_1316'),
        ('push_notifications', '0002_auto_20150807_0118'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntradayBigMovementReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent_change', models.DecimalField(default=0, verbose_name=b'% change at time of alert', max_digits=7, decimal_places=2)),
                ('timestamp', models.DateTimeField()),
                ('ticker', models.ForeignKey(to='satellite.Ticker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='rulesubscription',
            name='rule',
        ),
        migrations.RemoveField(
            model_name='rulesubscription',
            name='subscriber',
        ),
        migrations.DeleteModel(
            name='RuleSubscription',
        ),
        migrations.DeleteModel(
            name='TickerMovementRule',
        ),
        migrations.AddField(
            model_name='notificationsubscriber',
            name='services',
            field=models.ManyToManyField(to='satellite.Service', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notificationsubscriber',
            name='tickers_csv',
            field=models.CharField(max_length=400, null=True, blank=True),
            preserve_default=True,
        ),
    ]
