from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Follower)