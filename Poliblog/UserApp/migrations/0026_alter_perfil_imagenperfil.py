# Generated by Django 4.0.1 on 2022-02-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0025_remove_avatar_user_delete_lenguaje_delete_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='imagenPerfil',
            field=models.ImageField(default='PorDefecto/profileImageDefault.jpg', null=True, upload_to='avatares'),
        ),
    ]
