from django.contrib import admin
from .models import Post ,Comment ,File

# Register your models here.
class FileInLine(admin.TabularInline):
    model = File 
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [FileInLine]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(File)