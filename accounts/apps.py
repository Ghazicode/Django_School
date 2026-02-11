from django.apps import AppConfig
from django.contrib import admin


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "حساب"

    def ready(self):
        admin.site.site_title = "مدرسه امام حسین"
        admin.site.index_title = "پنل مدیریت"
