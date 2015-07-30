# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellite', '0030_article_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coveragetype',
            name='coverage_type',
            field=models.IntegerField(null=True, choices=[(1, b'10% Promise'), (2, b'Risk Rating'), (3, b'Guidance Change'), (4, b'5 and 3'), (5, b'10% Potential'), (6, b'2-Minute Drill'), (7, b'Best Buys Now'), (8, b'Team Preview'), (9, b'Team Review'), (10, b'Fool.com Preview'), (11, b'Fool.com Review'), (12, b'General Coverage')]),
            preserve_default=True,
        ),
    ]
