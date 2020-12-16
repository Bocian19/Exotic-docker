
from django.contrib import admin
from django.urls import include, path
from carparts.views import HomeView, ProductView, ProductsView, ContactView, BodykitsView, AboutView, LoadHiddenView, \
    SubscribeView, activate
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import debug_toolbar
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="main-page"),
    path('zapchasti/<str:slug>/', ProductView.as_view(),name="product"),
    path('zapchasti/<producer>/<pk>', ProductView.as_view(), name="product-step"),
    path('zapchasti/', ProductsView.as_view(), name="products"),
    path('kontakt/', ContactView.as_view(), name="contact"),
    path('load/', LoadHiddenView.as_view(), name="load-hidden"),
    path('о-компании/', AboutView.as_view(), name="about"),
    path('bodykits/', BodykitsView.as_view(), name="bodykits"),
    path('insta', TemplateView.as_view(template_name='instagram.html', extra_context={"instagram_profile_name": "exoticparts.eu"})),
    path('__debug__/', include(debug_toolbar.urls)),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        activate, name='activate'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
