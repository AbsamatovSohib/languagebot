# Generated by Django 5.0.6 on 2024-05-26 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=127, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=63, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='baza.book')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=127)),
                ('definition', models.CharField(blank=True, max_length=127, null=True)),
                ('tarjima', models.CharField(max_length=127)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baza.unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baza.user')),
            ],
        ),
    ]
