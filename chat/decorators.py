# -*- coding: utf-8 -*-

from functools import wraps
from rest_framework.response import Response
from django.utils.decorators import available_attrs
from django.core.exceptions import ObjectDoesNotExist

from .models import Account


def user_passes_test_400(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            error = test_func(request)
            if error is None:
                return view_func(request, *args, **kwargs)
            return Response(error, 400)
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator


def active_account_valid_func (request):
    if request.resource_owner is None:
        return "Invalid User"

    account_id = None

    if request.method == 'GET':
        account_id = request.GET.get('account')
    elif request.method == 'POST':
        account_id = request.POST.get('account')

    user = request.resource_owner
    if not account_id:
        a = Account.objects.filter(user=user, password__isnull=False).first()
        if a is None:
            return "No valid account found"
    else:
        try:
            a = Account.objects.get(user=user,id=account_id)
        except ObjectDoesNotExist:
            return "Invalid Account number provided (account=XXXX)"
    request.account = a
    return None


def active_account_required_400(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test_400(active_account_valid_func)
    if function:
        return actual_decorator(function)
    return actual_decorator

