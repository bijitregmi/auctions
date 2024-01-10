from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:pk>", views.listing, name="listing"),
    path("watchlist/<int:pk>", views.watchlist, name="watchlist"),
    path("bid/<int:pk>", views.bid, name="bid"),
    path("close/<int:pk>", views.close, name="close"),
    path("comment/<int:pk>", views.comment, name="comment"),
    path("watchlist_view", views.watchlist_view, name="watchlist_view"),
    path("categories", views.categories, name="categories"),
    path("category_view/<str:category>", views.category_view, name="category_view")
]
