# Generated by Django 5.0.6 on 2024-06-19 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laBiblioteca', '0002_alter_cliente_options_alter_cliente_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/', verbose_name='Portada'),
        ),
    ]
