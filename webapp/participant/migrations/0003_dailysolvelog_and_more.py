# Generated by Django 4.1.1 on 2022-09-05 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0002_remove_solvelog_is_success'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySolveLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='추가된 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 일시')),
                ('total_solved_count', models.IntegerField(default=0, verbose_name='푼 문제 수')),
                ('standard_date', models.DateField(verbose_name='해당 로그의 기준 날짜')),
                ('is_success', models.BooleanField(default=True)),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_solve_logs', to='participant.participant', verbose_name='참가자')),
            ],
            options={
                'verbose_name': 'DailySolveLog',
                'verbose_name_plural': 'DailySolveLogs',
                'db_table': 'daily_solve_logs',
            },
        ),
        migrations.AddConstraint(
            model_name='dailysolvelog',
            constraint=models.UniqueConstraint(fields=('participant', 'standard_date'), name='unique_daily_log_by_participant'),
        ),
    ]
