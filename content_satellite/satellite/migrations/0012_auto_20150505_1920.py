# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0011_ticker_services_for_ticker'),
    ]

    operations = [
        migrations.CreateModel(
            name='BylineMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('byline', models.CharField(max_length=50)),
                ('services', models.CharField(max_length=200, null=True, verbose_name=b'services covered in last year', blank=True)),
                ('tickers', models.CharField(max_length=1500, null=True, verbose_name=b'tickers covered in the last year', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='dataharvesteventlog',
            name='data_type',
            field=models.IntegerField(default=1, choices=[(1, b'articles'), (2, b'market performance'), (3, b'earnings dates'), (4, b'scorecard recs'), (5, b'bylines meta data')]),
            preserve_default=True,
        ),
    ]
