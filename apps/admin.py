from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html  # Rasmlarni ko'rsatish uchun
from modeltranslation.admin import TranslationAdmin

from apps.models import Sprint, Product, Feature, FeatureFile


# 1. Feature ichida fayllarni (rasmlarni) inline holatda boshqarish
class FeatureFileInline(admin.TabularInline):  # StackedInline o'rniga TabularInline joyni tejaydi
    model = FeatureFile
    extra = 1
    readonly_fields = ('get_preview',)

    def get_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 5px;" />',
                               obj.image.url)
        return "Rasm yo'q"

    get_preview.short_description = "Prevyu"


@admin.register(Sprint)
class SprintAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)  # Nomga bossa tahrirlashga kiradi
    search_fields = ('name',)
    ordering = ('-id',)  # Oxirgi qo'shilgan sprint yuqorida turadi


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('id', 'get_image', 'title')
    list_display_links = ('title',)
    search_fields = ('title',)

    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url)
        return "Rasm yo'q"

    get_image.short_description = "Rasm"


@admin.register(Feature)
class FeatureAdmin(TranslationAdmin):
    list_display = ('title', 'sprint', 'product')  # Agar created_at bo'lsa
    list_filter = ('sprint', 'product')  # Yon tomonda qulay filtr
    search_fields = ('title', 'description')
    autocomplete_fields = ('sprint', 'product')  # Agar ma'lumot ko'p bo'lsa, qidiruv bilan tanlash qulay
    inlines = [FeatureFileInline]


# Keraksiz Gruppalarni o'chirish
admin.site.unregister(Group)

# Admin panel sarlavhalarini o'zgartirish (ixtiyoriy)
admin.site.site_header = "SD Platform Admin"
admin.site.site_title = "SD Platform"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"
