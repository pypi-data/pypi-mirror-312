# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-Config-TUW hacks and overrides to be applied on application startup.

This module provides a blueprint whose sole purpose is to execute some code exactly
once during application startup (via ``bp.record_once()``).
These functions will be executed after the Invenio modules' extensions have been
initialized, and thus we can rely on them being already available.
"""

from logging import ERROR
from logging.handlers import SMTPHandler

from flask import Blueprint, current_app, flash, render_template, request
from flask_login import current_user, login_required
from flask_menu import register_menu
from invenio_db import db
from invenio_rdm_records.services.search_params import MyDraftsParam

from .curation import CurationForm
from .formatters import CustomFormatter


def register_smtp_error_handler(app):
    """Register email error handler to the application."""
    handler_name = "invenio-config-tuw-smtp-error-handler"

    # check reasons to skip handler registration
    error_mail_disabled = app.config.get("CONFIG_TUW_DISABLE_ERROR_MAILS", False)
    if app.debug or app.testing or error_mail_disabled:
        # email error handling should occur only in production mode, if not disabled
        return

    elif any([handler.name == handler_name for handler in app.logger.handlers]):
        # we don't want to register duplicate handlers
        return

    elif "invenio-mail" not in app.extensions:
        app.logger.warning(
            (
                "The Invenio-Mail extension is not loaded! "
                "Skipping registration of SMTP error handler."
            )
        )
        return

    # check if mail server and admin email(s) are present in the config
    # if not raise a warning
    if app.config.get("MAIL_SERVER") and app.config.get("MAIL_ADMIN"):
        # configure auth
        username = app.config.get("MAIL_USERNAME")
        password = app.config.get("MAIL_PASSWORD")
        auth = (username, password) if username and password else None

        # configure TLS
        secure = None
        if app.config.get("MAIL_USE_TLS"):
            secure = ()

        # initialize SMTP Handler
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config.get("MAIL_PORT", 25)),
            fromaddr=app.config["SECURITY_EMAIL_SENDER"],
            toaddrs=app.config["MAIL_ADMIN"],
            subject=app.config["THEME_SITENAME"] + " - Failure",
            credentials=auth,
            secure=secure,
        )
        mail_handler.name = handler_name
        mail_handler.setLevel(ERROR)
        mail_handler.setFormatter(CustomFormatter())

        # attach to the application
        app.logger.addHandler(mail_handler)

    else:
        app.logger.warning(
            "Mail configuration missing: SMTP error handler not registered!"
        )


def override_search_drafts_options(app):
    """Override the "search drafts" options to show all accessible drafts."""
    # doing this via config is (currently) not possible, as the `search_drafts`
    # property can't be overridden with a config item (unlike `search`, above it)
    # cf. https://github.com/inveniosoftware/invenio-rdm-records/blob/maint-10.x/invenio_rdm_records/services/config.py#L327-L332
    try:
        service = app.extensions["invenio-rdm-records"].records_service
        service.config.search_drafts.params_interpreters_cls.remove(MyDraftsParam)
    except ValueError:
        pass


def create_curation_settings_blueprint(app):
    """Register the curation settings view after the app has been initialized.

    This is necessary because we're depending on the Flask-Menu extension.
    """
    blueprint = Blueprint(
        "invenio_config_tuw_settings",
        __name__,
        url_prefix="/account/settings/curation",
    )

    @blueprint.route("/", methods=["GET", "POST"])
    @login_required
    @register_menu(
        blueprint,
        "settings.curation",
        '<i class="file icon"></i> Curation',
        order=1,
    )
    def curation_settings_view():
        preferences_curation_form = CurationForm(
            formdata=None, obj=current_user, prefix="preferences-curation"
        )

        form_name = request.form.get("submit", None)
        form = preferences_curation_form if form_name else None

        if form:
            form.process(formdata=request.form)
            if form.validate_on_submit():
                form.populate_obj(current_user)
                db.session.add(current_user)
                current_app.extensions["security"].datastore.commit()
                flash(("Curation settings were updated."), category="success")

        return render_template(
            "invenio_theme_tuw/settings/curation.html",
            preferences_curation_form=preferences_curation_form,
        )

    return blueprint
