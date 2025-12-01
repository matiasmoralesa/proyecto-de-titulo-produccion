# Generated migration for TelegramLinkCode model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('omnichannel_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramLinkCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=6, unique=True)),
                ('chat_id', models.CharField(blank=True, max_length=200)),
                ('is_used', models.BooleanField(default=False)),
                ('expires_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
            options={
                'db_table': 'telegram_link_codes',
                'ordering': ['-created_at'],
            },
        ),
    ]
