# Generated by Django 3.2.10 on 2022-06-23 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1, '一般'), (2, '重要'), (3, '紧急')], default=2, verbose_name='级别')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='任务详情')),
                ('adminuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.admin', verbose_name='负责人')),
            ],
        ),
    ]
