from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

#Custom decorators for manager and standard users (implemented in views.py)

'''
Decorator for views that checks that the logged in user is a manager,
redirects to the log-in page if necessary.
'''
def manager_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    #Check basic user requirements first
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_manager,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

'''
Decorator for views that checks that the logged in user is a standard user,
redirects to the log-in page if necessary.
'''
def standardUser_required(function = None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    #Check basic user requirements first
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_standard,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
