# Generated by Django 3.1.5 on 2021-04-08 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0002_doctor_username'),
        ('accounts', '0002_auto_20210402_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.IntegerField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='doctors.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.user')),
            ],
        ),
    ]