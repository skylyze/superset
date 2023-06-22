import logging
import urllib.parse
from urllib.parse import quote

from flask import redirect, request
from flask_appbuilder.security.manager import AUTH_OID
from flask_appbuilder.security.views import AuthOIDView
from flask_appbuilder.views import expose, ModelView, SimpleFormView
from flask_login import login_user
from flask_oidc import OpenIDConnect
import os

from superset.security import SupersetSecurityManager

LOG = logging.getLogger(__name__)


class OIDCSecurityManager(SupersetSecurityManager):
    def __init__(self, appbuilder):
        super(OIDCSecurityManager, self).__init__(appbuilder)
        if self.auth_type == AUTH_OID:
            self.oid = OpenIDConnect(self.appbuilder.get_app)
        self.authoidview = AuthOIDCView


class AuthOIDCView(AuthOIDView):
    @expose("/login/", methods=["GET", "POST"])
    def login(self, flag=True):
        sm = self.appbuilder.sm
        oidc = sm.oid

        @self.appbuilder.sm.oid.require_login
        def handle_login():
            user = sm.auth_user_oid(oidc.user_getfield("email"))
            info = oidc.user_getinfo(
                ["preferred_username", "given_name", "family_name", "email"]
            )
            keycloak_user_details = {
                "username": info.get("preferred_username"),
                "first_name": info.get("given_name"),
                "last_name": info.get("family_name"),
                "email": info.get("email"),
            }
            superset_roles = []
            try:
                superset_roles = oidc.user_getfield(field="realm_access_roles")
                superset_roles = list(
                    map(lambda x: x if "Superset" in x else None, superset_roles)
                )
                superset_roles = [
                    role.replace("Superset", "")
                    for role in superset_roles
                    if role is not None
                ]
            except Exception as e:
                LOG.error(e)
            roles = superset_roles if len(superset_roles) > 0 else ["Gamma"]
            sm_roles = []
            for role in roles:
                try:
                    sm_roles.append(sm.find_role(role))
                except Exception as e:
                    LOG.error(e)
            keycloak_user_details["superset_roles"] = set(sm_roles)

            if user is None:
                user = sm.add_user(
                    username=keycloak_user_details["username"],
                    first_name=keycloak_user_details["first_name"],
                    last_name=keycloak_user_details["last_name"],
                    email=keycloak_user_details["email"],
                    role=sm_roles,
                )
            superset_user_details = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "superset_roles": set(user.roles),
            }

            if keycloak_user_details != superset_user_details:
                user.roles = sm_roles
                user.first_name = keycloak_user_details["first_name"]
                user.last_name = keycloak_user_details["last_name"]
                user.email = keycloak_user_details["email"]
                sm.update_user(user=user)
                LOG.info(
                    f"updated user {superset_user_details['first_name']} {superset_user_details['last_name']}"
                )
            login_user(user, remember=False)

            return redirect(self.appbuilder.get_url_for_index)

        return handle_login()

    @expose("/logout/", methods=["GET", "POST"])
    def logout(self):
        oidc = self.appbuilder.sm.oid

        oidc.logout()
        super(AuthOIDCView, self).logout()
        # redirect_url = urllib.parse.quote_plus(request.url_root.strip("/") + self.appbuilder.get_url_for_login)
        FQDN = os.getenv("FQDN")
        redirect_url = f"http://{FQDN}:8088/login"

        return redirect(
            oidc.client_secrets.get("issuer")
            + "/protocol/openid-connect/logout?client_id="
            + oidc.client_secrets.get("client_id")
            + "&post_logout_redirect_uri="
            + quote(redirect_url)
        )
