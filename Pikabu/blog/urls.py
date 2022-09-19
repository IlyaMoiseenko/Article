from django.urls import path
from blog import views


urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),

    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('user-articles', views.ArticleCreateView.as_view(), name='user-articles'),
    path('article-edit/<int:pk>', views.ArticleEditView.as_view(), name='article-edit'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='article-delete'),

    path('sign-in', views.SignInView.as_view(), name='sign-in'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('log-out', views.LogoutView.as_view(), name='log-out')
]