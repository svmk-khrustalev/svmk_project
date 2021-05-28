
from django.urls import path
from account.views import login_view, logout_view, account_view, reg_view, post_new, ProductsDetailView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from account.models import Post
from account import views
app_name = 'account'

urlpatterns = [
    path('reg/', reg_view, name='reg'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', post_new, name='add'),
    path('', account_view, name='home'),
    path('account/<pk>/', ProductsDetailView.as_view(model=Post), name="Product_single"),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)