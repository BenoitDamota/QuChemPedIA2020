# Generated by Django 2.2.16 on 2020-09-28 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_auto_20200928_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moleculelong',
            old_name='basis_set_md5',
            new_name='basis_set_name',
        ),
    ]
