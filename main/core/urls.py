from django.urls import path

from . import views

urlpatterns = [
    #     path('', views.home, name='home'),
    #     path('detail/', views.detail_page, name='detail_page'),
    path('', views.HomeListView.as_view(), name='home'),
    path('detail/<slug:slug>', views.HomeDetailView.as_view(), name='detail_page'),
    path('edit-page', views.ArticleCreateView.as_view(), name='edit_page'),
    # path('edit-page', views.edit_page, name='edit_page'),
    path('update-page/<slug:slug>', views.ArticleUpdateView.as_view(), name='update_page'),
    # path('update-page/<slug:slug>', views.update_page, name='update_page'),
    path('delete-page/<slug:slug>', views.ArticleDeleteView.as_view(), name='delete_page'),
    # path('delete-page/<slug:slug>', views.delete_page, name='delete_page'),
    path('login', views.MyLoginView.as_view(), name='login_page'),
    path('register', views.RegisterUserView.as_view(), name='register_page'),
    path('logout', views.MyLogoutView.as_view(), name='logout_page'),
]
