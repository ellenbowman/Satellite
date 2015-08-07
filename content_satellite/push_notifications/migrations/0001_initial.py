# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationSubscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Contact Name')),
                ('slack_handle', models.CharField(max_length=30)),
                ('email_address', models.EmailField(max_length=30, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RuleSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_preference_asap', models.BooleanField(default=True, verbose_name=b'push an alert as soon as the condition is satisfied (vs end of day)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TickerMovementRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticker_symbol', models.CharField(max_length=10)),
                ('threshold', models.IntegerField(default=7, verbose_name=b'percent change')),
                ('condition', models.CharField(default=(b'gt', b'greater than'), max_length=5, choices=[(b'gt', b'greater than'), (b'lt', b'less than')])),
                ('is_satisfied_today', models.BooleanField(default=False, verbose_name=b'has the condition been satisfied today?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rulesubscription',
            name='rule',
            field=models.ForeignKey(to='push_notifications.TickerMovementRule'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rulesubscription',
            name='subscriber',
            field=models.ForeignKey(to='push_notifications.NotificationSubscriber'),
            preserve_default=True,
        ),
    ]
