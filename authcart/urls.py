from django.urls import path
from authcart import views

urlpatterns = [
    path('signup/',views.signup, name="signup"),
    path('login/',views.login_user, name="login_user"),
    path('logout/',views.logout_user, name="logout_user"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),
         name='activate'),
    path('RequestResetEmail/',views.RequestResetEmailView.as_view(),name='RequestResetEmail'),
    path('setNewPassword/<str:uid64>/<str:token>',views.SetNewPasswordView.as_view(),name='SetNewPassword')
]
