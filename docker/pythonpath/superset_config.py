import os

import keycloack_security_manager
from flask import redirect
from flask_appbuilder import expose, IndexView
from flask_appbuilder.const import AUTH_OID

from dataset_translations import include_language
from superset.superset_typing import FlaskResponse

lang_trans = include_language()

LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "de": {"flag": "de", "name": "Deutsch"},
}

ENABLE_CORS = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
ENABLE_PROXY_FIX = True
WTF_CSRF_ENABLED = True
AUTH_ROLE_PUBLIC = "Public"
PUBLIC_ROLE_LIKE_GAMMA = True
GUEST_ROLE_NAME = "Gamma"
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "DASHBOARD_FILTERS_EXPERIMENTAL": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DRUID_JOINS": True,
    "CACHE_QUERY_BY_USER": False,
}

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"],
}


# ---------------------------KEYCLOACK ----------------------------

curr = os.path.abspath(os.getcwd())
FQDN = os.getenv("FQDN")
SCHEME = os.getenv("SCHEME")
OIDC_CLIENT_SECRETS = curr + "/pythonpath/client_secret.json"

AUTH_TYPE = AUTH_OID
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_REQUIRE_VERIFIED_EMAIL = False
OIDC_CLOCK_SKEW = 700
OIDC_OPENID_REALM = "skytroll"
OIDC_INTROSPECTION_AUTH_METHOD = "client_secret_post"
CUSTOM_SECURITY_MANAGER = keycloack_security_manager.OIDCSecurityManager
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"
OIDC_VALID_ISSUERS = [f"{SCHEME}://{FQDN}/auth/realms/skytroll", f"{SCHEME}://{FQDN}"]


# Changing default landing page

# Specify the environment variable name
landing_page_env_var_name = "LANDING_PAGE_URL"

# Set the default value for landing page
landing_page_url = "/superset/welcome/"

# Retrieve the environment variable value or use the default value
landing_page_url = os.environ.get(landing_page_env_var_name, landing_page_url)


class SupersetLandingPage(IndexView):
    @expose("/")
    def index(self) -> FlaskResponse:
        return redirect(landing_page_url)


FAB_INDEX_VIEW = f"{SupersetLandingPage.__module__}.{SupersetLandingPage.__name__}"
