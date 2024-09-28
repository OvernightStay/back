from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.PlayerRegisterViewSet.as_view(), name='register'),
	path('login/', views.PlayerLoginViewSet.as_view(), name='login'),
 	# path('verify/', views.VerifyCodeViewSet.as_view(), name='verify'),
	path('logout/', views.PlayerLogoutViewSet.as_view(), name='logout'),
	path('player/', views.PlayerViewSet.as_view(), name='player'),
 	path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('item/', views.ItemViewSet.as_view()),
    path('backpack/', views.BackpackViewSet.as_view()),
    path('backpack_item/', views.BackpackItemViewSet.as_view()),
]
