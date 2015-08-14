# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataImportLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticker_count', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
                ('comments', models.CharField(max_length=500)),
                ('meta', models.CharField(max_length=500, null=True, blank=True)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('function_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=250)),
                ('list_order', models.IntegerField()),
                ('hint', models.ForeignKey(to='risk_ratings.Hint', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RiskRatingDraft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionnaire_name', models.CharField(max_length=50)),
                ('ticker_symbol', models.CharField(max_length=10)),
                ('responses_json', models.TextField()),
                ('meta', models.CharField(max_length=100, null=True, blank=True)),
                ('crushability_count', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RiskRatingRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('legacy_uri', models.URLField()),
                ('publish_date', models.DateField()),
                ('headline', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('symbol', models.CharField(max_length=10)),
                ('exchange', models.CharField(max_length=10)),
                ('company_name', models.CharField(max_length=200)),
                ('instrument_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TickerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hq_city', models.CharField(max_length=100, null=True, blank=True)),
                ('hq_state', models.CharField(max_length=100, null=True, blank=True)),
                ('hq_country', models.CharField(max_length=100, null=True, blank=True)),
                ('year_founded', models.IntegerField(null=True, blank=True)),
                ('ceo_name', models.CharField(max_length=100, null=True, blank=True)),
                ('net_income_ltm', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('net_income_years_ago_1', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('net_income_years_ago_2', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('net_income_years_ago_3', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('net_income_years_ago_4', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('net_income_years_ago_5', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('net_income_mrq', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('free_cash_flow_ltm', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('free_cash_flow_years_ago_1', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('free_cash_flow_years_ago_2', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('free_cash_flow_years_ago_3', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('operating_cash_ltm', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('operating_cash_mrq', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('compound_annual_growth_rate_3_year', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('market_cap', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('total_debt', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('debt_to_equity', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('cash_incl_st_investments', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('roe_ltm', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('roe_years_ago_1', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('roe_years_ago_2', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('roe_years_ago_3', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('roe_years_ago_4', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('roe_years_ago_5', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('roe_mrq', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('beta_ltm', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('stock_price', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('earnings_per_share', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('price_per_earnings', models.DecimalField(default=0, max_digits=12, decimal_places=2)),
                ('insider_holdings_1', models.DecimalField(default=-1, max_digits=10, decimal_places=5)),
                ('insider_holdings_2', models.DecimalField(default=-1, max_digits=10, decimal_places=5)),
                ('insider_holdings_3', models.DecimalField(default=-1, max_digits=10, decimal_places=5)),
                ('insider_holdings_4', models.DecimalField(default=-1, max_digits=10, decimal_places=5)),
                ('insider_holdings_5', models.DecimalField(default=-1, max_digits=10, decimal_places=5)),
                ('competitors', models.CharField(max_length=500, null=True, blank=True)),
                ('date_last_synced', models.DateTimeField()),
                ('ticker', models.ForeignKey(to='risk_ratings.Ticker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='riskratingrecord',
            name='ticker',
            field=models.ForeignKey(to='risk_ratings.Ticker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(to='risk_ratings.Questionnaire'),
            preserve_default=True,
        ),
    ]
