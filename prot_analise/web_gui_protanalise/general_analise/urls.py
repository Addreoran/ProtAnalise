from django.urls import path

from . import views

app_name = 'general_analise'
urlpatterns = [
    path('analise/', views.FormView.as_view(), name='form'),
    path('loads/', views.LoadsView.as_view(), name='loads'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('<int:pk>/<str:group>/<str:king>/<int:cluster_pk>', views.DetailCellularView.as_view(),
         name='detail_cellular'),
    path('', views.HomeView.as_view(), name='home'),
]
