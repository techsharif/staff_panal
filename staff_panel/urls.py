from django.conf.urls import url

from staff_panel.views import StaffLogin, StaffLogout, EmailSubmissionForPasswordChange, \
    StaffForgotPassword, StaffChangePassword, Home

urlpatterns = [
    url(r'^login/$', StaffLogin.as_view(), name='staff_panel_login'),
    url(r'^$', Home.as_view(), name='staff_panel_home'),
    url(r'^logout/$', StaffLogout.as_view(), name='staff_panel_logout'),
    url(r'^submit-email/$', EmailSubmissionForPasswordChange.as_view(), name='email-submission'),
    url(r'^forgot-password/(?P<code>[a-zA-Z0-9]+)$', StaffForgotPassword.as_view(), name='staff_panel_forgot_password'),
    url(r'^password-change/$', StaffChangePassword.as_view(), name='staff_panel_password_change'),
]
