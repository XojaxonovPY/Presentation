from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from apps.models import Sprint, Product, Feature, FeatureFile


class FeatureFileInline(admin.TabularInline):
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
class SprintAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('-id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'sprint', 'product')
    list_filter = ('sprint', 'product')
    search_fields = ('title', 'description')
    autocomplete_fields = ('sprint', 'product')
    inlines = [FeatureFileInline]


admin.site.unregister(Group)
admin.site.site_header = "SD Platform Admin"
admin.site.site_title = "SD Platform"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"
