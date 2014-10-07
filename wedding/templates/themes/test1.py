from django.conf import settings
import os.path
from django.utils.translation import ugettext_lazy as _ 
from django.utils.safestring import mark_safe

for i in range(1, 31) :
    print '("theme%s", mark_safe(_("<img src="(media_url)images/themes/theme%s.jpg" alt="theme%s" title="Theme%s">" {"media_url": settings.MEDIA_URL, },))),' % (i, i, i, i)
