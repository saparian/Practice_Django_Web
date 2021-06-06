"""HP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views 일 경우
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views 일 경우
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf # 다른 참조할 URL file 들을 포함시켜야 하는 경우
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

#Use include() to add paths from the catalog application
#www.xxxx.com/catalog로 시작되는 요청이 올때 catalog/urls.py를 참조해서 맵핑하겠다는 코드
from django.conf.urls import include
from django.urls import path

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]

#Add URL maps to redirect the base URL to our application
#'/catalog/'로 리다이렉트하기 위한 코드
from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]  #첫 매개변수에 ''을 비워놓으면 '/'를 의미


#Use static() to add rul mapping to serve static files during development (only)
#CSS, JavaScript, image 같은 정적인 파일을 제공하게 해주는 코드
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
