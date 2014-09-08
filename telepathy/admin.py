from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.galleries.admin import GalleryAdmin
from telepathy import models



class ProjectImageInline(TabularDynamicInlineAdmin):
    model = models.ProjectImage


class ProjectAdmin(PageAdmin):
    inlines = (ProjectImageInline, )


admin.site.register(models.Project, ProjectAdmin)
