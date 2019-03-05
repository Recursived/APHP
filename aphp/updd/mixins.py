import inspect

from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.encoding import force_text
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

class AccessMixin(object):
    """
    'Abstract' mixin that gives access mixins the same customizable
    functionality.
    """
    login_url = None
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
    redirect_unauthenticated_users = False

    def get_login_url(self):
        """
        Override this method to customize the login_url.
        """
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                'Define {0}.login_url or settings.LOGIN_URL or override '
                '{0}.get_login_url().'.format(self.__class__.__name__))

        return force_text(login_url)

    def get_redirect_field_name(self):
        """
        Override this method to customize the redirect_field_name.
        """
        if self.redirect_field_name is None:
            raise ImproperlyConfigured(
                '{0} is missing the '
                'redirect_field_name. Define {0}.redirect_field_name or '
                'override {0}.get_redirect_field_name().'.format(
                    self.__class__.__name__))
        return self.redirect_field_name

    def handle_no_permission(self, request):
        if self.raise_exception:
            if (self.redirect_unauthenticated_users
                    and not request.user.is_authenticated):
                return self.no_permissions_fail(request)
            else:
                if (inspect.isclass(self.raise_exception)
                        and issubclass(self.raise_exception, Exception)):
                    raise self.raise_exception
                if callable(self.raise_exception):
                    ret = self.raise_exception(request)
                    if isinstance(ret, (HttpResponse, StreamingHttpResponse)):
                        return ret
                raise PermissionDenied

        return self.no_permissions_fail(request)

    def no_permissions_fail(self, request=None):
        """
        Called when the user has no permissions and no exception was raised.
        This should only return a valid HTTP response.
        By default we redirect to login.
        """
        return redirect_to_login(request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())

class GroupRequiredMixin(AccessMixin):
    group_required = None
    login_url = 'login'

    def get_group_required(self):
        if self.group_required is None or (
                not isinstance(self.group_required,
                               (list, tuple))
        ):
            raise ImproperlyConfigured(
                '{0} requires the "group_required" attribute to be set and be '
                'one of the following types: list or '
                'tuple'.format(self.__class__.__name__))
        if not isinstance(self.group_required, (list, tuple)):
            self.group_required = (self.group_required,)
        return self.group_required

    def check_membership(self, groups):
        """ Check required group(s) """
        if self.request.user.is_superuser:
            return True
        user_groups = self.request.user.groups.values_list("name", flat=True)
        return set(groups).intersection(set(user_groups))

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        in_group = False
        if request.user.is_authenticated:
            in_group = self.check_membership(self.get_group_required())
        else:
            messages.error(request, _("Il faut être connnecté pour pouvoir accéder à cette page !"))

        if not in_group:
            messages.error(request,_("Vous n'avez pas le statut nécéssaire pour accéder à cette page !"))
            self.login_url = 'accueil'
            return self.handle_no_permission(request)
        return super(GroupRequiredMixin, self).dispatch(
            request, *args, **kwargs)