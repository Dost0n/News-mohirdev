from django.urls import path
from accounts.views import user_login, profile, user_register, SignUpView, edit_user, Edit_UserView, admin_page
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                        PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)


urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('password-change/', PasswordChangeView.as_view(), name = 'password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('password-reset/', PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('profile/', profile, name= 'profile'),
    path('signup/', user_register, name= 'signup'),
    path('registration/', SignUpView.as_view(), name= 'registration'),
    path('profileedit', Edit_UserView.as_view(), name= 'profile-edit'),
    path('editprofile', edit_user, name= 'edit-profile'),
    path('admin-page', admin_page, name= 'admin-page'),
]