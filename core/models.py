from django.db import models


class SiteSettings(models.Model):
    """Site-wide settings editable from admin"""

    # Contact Info
    email = models.EmailField(default='hello@nomadsocks.com')
    phone = models.CharField(max_length=50, blank=True, default='+976 9999 9999')

    # Address
    address = models.CharField(max_length=200, blank=True, default='Ulaanbaatar, Mongolia')
    address_mn = models.CharField(max_length=200, blank=True, default='Улаанбаатар, Монгол')

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    # About text (for footer)
    tagline = models.CharField(max_length=200, default='Quality socks from Mongolia')
    tagline_mn = models.CharField(max_length=200, default='Монголын чанартай оймс')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
