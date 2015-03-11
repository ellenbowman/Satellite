# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('date_pub', models.DateField(null=True, blank=True)),
                ('url', models.URLField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scorecard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('pretty_name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceTake',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_first', models.BooleanField(default=False)),
                ('is_newest', models.BooleanField(default=False)),
                ('action', models.CharField(max_length=10)),
                ('is_core', models.BooleanField(default=False)),
                ('is_present', models.BooleanField(default=False)),
                ('scorecard', models.ForeignKey(to='satellite.Scorecard')),
                ('ticker', models.ForeignKey(to='satellite.Ticker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scorecard',
            name='service',
            field=models.ForeignKey(to='satellite.Service'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='service',
            field=models.ForeignKey(to='satellite.Service'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='ticker',
            field=models.ForeignKey(to='satellite.Ticker'),
            preserve_default=True,
        ),
    ]
