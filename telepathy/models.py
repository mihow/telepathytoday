from string import punctuation
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from mezzanine.pages.models import Page
from mezzanine.core.models import RichText, Orderable
from mezzanine.core.fields import FileField
from mezzanine.utils.models import upload_to



class Project(Page, RichText):
    secondary_content = models.TextField(blank=True)


#@python_2_unicode_compatible
class Image(models.Model):
    ''' Copied from mezzanine.galleries.models.GalleryImage '''

    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("galleries.GalleryImage.file", "galleries"))
    description = models.CharField(_("Description"), max_length=1000, blank=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description:
            name = force_text(self.file.name)
            name = name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(Image, self).save(*args, **kwargs)


class ProjectImage(Orderable, Image):
    project = models.ForeignKey("Project", related_name="images")

    class Meta:
        verbose_name = _("Project Image")
