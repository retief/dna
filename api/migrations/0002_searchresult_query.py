# Generated by Django 3.1.3 on 2020-11-14 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='query',
            field=models.CharField(default='aatcaac', max_length=100),
            preserve_default=False,
        ),
    ]
