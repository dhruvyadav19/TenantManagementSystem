# Generated by Django 3.1.1 on 2020-11-09 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('houses', '0012_contract'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_date', models.DateField(auto_now_add=True)),
                ('complaint_type', models.CharField(choices=[('PL', 'Plumbing'), ('EL', 'Electrical'), ('Rv', 'Renovation'), ('Ot', 'Others')], default='Ot', max_length=200)),
                ('complaint', models.CharField(blank=True, max_length=200)),
                ('house', models.ForeignKey(default=19, on_delete=django.db.models.deletion.CASCADE, to='houses.house')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]