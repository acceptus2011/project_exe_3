"""
URL configuration for project_exe_3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from myapp.views import ReturnCreateView, ReturnApproveView, ReturnDeclineView, ProductCreateView, ReturnListView

from myapp.views import RegisterView, ProductListView, PurchaseView, ProfileView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', ProductListView.as_view(), name='index'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create-return/', ReturnCreateView.as_view(), name='create_return'),
    path('return-approve/<int:pk>', ReturnApproveView.as_view(), name='return_approve'),
    path('return-decline/<int:pk>', ReturnDeclineView.as_view(), name='return_decline'),
    path('product-create/', ProductCreateView.as_view(), name='product_create'),
    path('return_list/', ReturnListView.as_view(), name='returns_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


