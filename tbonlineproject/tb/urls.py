from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('tb.views',
    url(r'^faq/$', TemplateView.as_view(template_name="patient_info.html"),name="tb_patient_info"),
)
