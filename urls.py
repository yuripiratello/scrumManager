from django.conf.urls.defaults import *
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^scrumManager/', include('scrumManager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'core.views.scrumBoard'),

    (r'^changeTaskStatus/', 'core.views.updateTaskStatus'),
    (r'^pegarTask/', 'core.views.updateTaskSprintResponsible'),

    (r'^lancarHora/', 'core.views.lancarHora'),
    (r'^comentarios/', 'core.views.comentarios'),

    url(r'^login/$',  'django.contrib.auth.views.login', {'template_name' : 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/login/'}, name='logout'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root' : settings.MEDIA_ROOT}),

)
