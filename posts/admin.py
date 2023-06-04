from django.contrib import admin

from .models import Posts

@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'posted_date')
    list_filter = ('status',)
    actions = ('publish', 'unpublish')

    def publish(self, request, queryset):
        queryset.update(status=Posts.PostStatus.PUBLISHED)

    publish.short_description = "Publish Selected"

    def unpublish(self, request, queryset):
        queryset.update(status=Posts.PostStatus.UNPUBLISHED)

    unpublish.short_description = "Unpublish Selected"



