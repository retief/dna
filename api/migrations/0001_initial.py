# Generated by Django 3.1.3 on 2020-11-14 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=40)),
                ('protein', models.CharField(blank=True, max_length=10)),
                ('location', models.IntegerField(null=True)),
                ('feature_location', models.CharField(blank=True, max_length=50)),
                ('protein_id', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
