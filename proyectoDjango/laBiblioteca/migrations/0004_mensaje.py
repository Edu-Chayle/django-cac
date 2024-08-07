# Generated by Django 5.0.6 on 2024-06-20 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laBiblioteca', '0003_alter_libro_portada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=160, verbose_name='Nombre')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('mensaje', models.CharField(max_length=500, verbose_name='Mensaje')),
                ('recibir_noticias', models.BooleanField(blank=True, verbose_name='Suscribirse a noticias')),
            ],
        ),
    ]
