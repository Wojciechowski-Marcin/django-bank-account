from django.urls import path, re_path
from . import views as client_views

urlpatterns = [
    path('',
         client_views.home,
         name='home'),
    path('send_request/',
         client_views.send_request,
         name='send_request'),
    path('my_requests/',
         client_views.my_requests,
         name='my_requests'),
    re_path(r'^my_requests/user_request_details/(?P<rid>[0-9]+)/$',
            client_views.user_request_details,
            name='user_request_details'),
    path('open_account/',
         client_views.open_account,
         name='open_account'),
    path('make_transaction/',
         client_views.make_transaction,
         name='make_transaction'),
    path('open_credit_account/',
         client_views.open_credit_account,
         name='open_credit_account'),
    path('request_credit_card/',
         client_views.request_credit_card,
         name='request_credit_card'),
    re_path(r'^account/(?P<oid>[0-9]+)/$',
            client_views.account,
            name='account'),
    re_path(r'^account/(?P<oid>[0-9]+)/edit_account$',
            client_views.edit_account,
            name='edit_account'),
    re_path(r'^account/(?P<oid>[0-9]+)/delete_account$',
            client_views.delete_account,
            name='delete_account'),
    re_path(r'^account/(?P<oid>[0-9]+)/transaction_history$',
            client_views.transaction_history,
            name='transaction_history'),
    re_path(r'^account/(?P<oid>[0-9]+)/order_card$',
            client_views.order_card,
            name='order_card'),
    re_path(r'^account/(?P<oid>[0-9]+)/card/(?P<coid>[0-9]+)$',
            client_views.card,
            name='card'),
    re_path(r'^account/(?P<oid>[0-9]+)/card/(?P<coid>[0-9]+)/edit_card$',
            client_views.edit_card,
            name='edit_card'),
    re_path(r'^account/(?P<oid>[0-9]+)/card/(?P<coid>[0-9]+)/delete_card$',
            client_views.delete_card,
            name='delete_card'),
]
