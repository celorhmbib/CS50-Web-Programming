from django.urls import path

from .views import index, entry_page,create_entry,update_entry,random_entry,delete_entry

urlpatterns = [
    path("", index.as_view(), name="index"),
    path('wiki/<str:title>/', entry_page.as_view(), name="entry_page"),
    path("add_entry/", create_entry.as_view(), name="create_entry"),
    path('wiki/update/<str:title>/', update_entry.as_view(), name="update_entry"),
    path('random_entry/', random_entry.as_view(), name="random_entry"),
    path('wiki/delete/<str:title>/', delete_entry.as_view(), name="delete_entry")
]
