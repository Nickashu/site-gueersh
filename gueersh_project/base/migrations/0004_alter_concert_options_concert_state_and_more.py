# Generated by Django 5.2 on 2025-04-26 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_band_info_contact_booking_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='concert',
            options={'verbose_name': 'Concert', 'verbose_name_plural': 'Concerts'},
        ),
        migrations.AddField(
            model_name='concert',
            name='state',
            field=models.CharField(blank=True, default='', help_text='Estado onde o show ocorrerá (pode deixar em branco). Ex: SP', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='concert',
            name='city',
            field=models.CharField(default='', help_text='Cidade onde o show ocorrerá. Ex: São Paulo', max_length=100),
        ),
    ]
