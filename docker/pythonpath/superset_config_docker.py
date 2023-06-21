import os

from flask_appbuilder.const import AUTH_OID
import keycloack_security_manager

ENABLE_CORS = True
SESSION_COOKIE_SAMESITE = "Lax"
# SESSION_COOKIE_SECURE = False # uncomment this for the superset sdk use-case
SESSION_COOKIE_SECURE = False

SESSION_COOKIE_HTTPONLY = False
ENABLE_PROXY_FIX = True
# WTF_CSRF_ENABLED = False # uncomment this for the superset sdk use-case
WTF_CSRF_ENABLED = True
# CSRF_ENABLED = False # uncomment this for the superset sdk use-case
# PUBLIC_ROLE_LIKE = "Gamma"
AUTH_ROLE_PUBLIC = "Public"
PUBLIC_ROLE_LIKE_GAMMA = True
GUEST_ROLE_NAME = "Gamma"
FEATURE_FLAGS = {
    # "CLIENT_CACHE": True,
    "ALERT_REPORTS": True,
    # "EMBEDDED_SUPERSET": True,
    # "EMBEDDABLE_CHARTS": True,
    # "DASHBOARD_CROSS_FILTERS": True,
    # "DASHBOARD_RBAC": True,
    "DASHBOARD_FILTERS_EXPERIMENTAL": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DRUID_JOINS": True,
    "CACHE_QUERY_BY_USER": False,
}
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@database:5432/superset'

CORS_OPTIONS = {"supports_credentials": True, "allow_headers": ["*"], "resources": ["*"], "origins": ["*"]}

"""
---------------------------KEYCLOACK ----------------------------
"""
curr = os.path.abspath(os.getcwd())
AUTH_TYPE = AUTH_OID
OIDC_CLIENT_SECRETS = curr + "/docker/pythonpath_dev/client_secret.json"
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_REQUIRE_VERIFIED_EMAIL = False
OIDC_CLOCK_SKEW = 700
OIDC_OPENID_REALM: "master"
OIDC_INTROSPECTION_AUTH_METHOD: "client_secret_post"
CUSTOM_SECURITY_MANAGER = keycloack_security_manager.OIDCSecurityManager
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"
OIDC_VALID_ISSUERS = ["http://localhost:8090/realms/skytroll"]
"""
--------------------------------------------------------------
"""
# fix(dashbaord)
