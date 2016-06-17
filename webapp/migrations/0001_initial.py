# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 10:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('voornaam', models.CharField(max_length=128)),
                ('naam', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128, unique=True)),
                ('activation_key', models.CharField(max_length=40)),
                ('key_expires', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('straatnaam', models.CharField(max_length=128)),
                ('huisnr', models.IntegerField()),
                ('busnr', models.CharField(blank=True, max_length=10, null=True)),
                ('telefoonnr', models.IntegerField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=255)),
                ('data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
                ('voornaam', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=128)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('thumbnail', models.BooleanField(default=False)),
                ('docfile', models.FileField(blank=True, upload_to=b'documents/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='GoedDoel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=128)),
                ('bijschrift', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=255)),
                ('foto_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Handelstatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('logText', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referentienummer', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('straatnaam', models.CharField(max_length=128)),
                ('huisnr', models.SmallIntegerField()),
                ('busnr', models.CharField(blank=True, max_length=10, null=True)),
                ('beschrijving', models.CharField(blank=True, max_length=1000, null=True)),
                ('uitgelicht', models.BooleanField(default=False)),
                ('prijs', models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ('thumbnail_url', models.CharField(blank=True, max_length=256, null=True)),
                ('handelstatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Handelstatus')),
            ],
        ),
        migrations.CreateModel(
            name='PandReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=128)),
                ('auteur', models.CharField(max_length=128)),
                ('text', models.CharField(max_length=500)),
                ('rating', models.CharField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')], default=5, max_length=2)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=128)),
                ('onderschrift', models.CharField(max_length=255)),
                ('foto_url', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Stad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postcode', models.CharField(max_length=12)),
                ('stadsnaam', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='StatusBericht',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=255)),
                ('inhoud', models.TextField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagnaam', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='TagPand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('pand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Pand')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Voortgang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='pand',
            name='postcodeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Stad'),
        ),
        migrations.AddField(
            model_name='pand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pand',
            name='voortgang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Voortgang'),
        ),
        migrations.AddField(
            model_name='foto',
            name='pand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Pand'),
        ),
        migrations.AddField(
            model_name='user',
            name='postcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Stad'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
