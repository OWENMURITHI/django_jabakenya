
from django.urls import path
from .views import products
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', products.ProductView.as_view(), name='home'),
    path('search/', products.search, name='search'),
    path('add_product/', products.ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/', products.ProductDetail.as_view(), name='product_page'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

   
