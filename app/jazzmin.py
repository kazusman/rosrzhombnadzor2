import os

JAZZMIN_SETTINGS = {
    "site_title": "РосРжомбНадзор",
    "site_header": "РосРжомбНадзор",
    "site_logo": "jazzmin/img/logo.png",
    "site_icon": "jazzmin/img/favicon.ico",
    "welcome_sign": "Добро пожаловать в РосРжомбНадзор",
    "copyright": "РЖАКА РЖОМБА РЖУЛЬКА",
    "user_avatar": "jazzmin/img/logo.png",
    "search_model": None,
    "topmenu_links": [
        {"name": "Home", "url": "/admin"},
        {"name": "Open bot", "url": os.getenv("BOT_URL"), "new_window": True},
        {"name": "Set webhook", "url": f"/bot/set_webhook/"},
        {"app": "bot"},
    ],
    "usermenu_links": None,
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["bot", "google_vision"],
    "custom_links": {
        "bot": [
            {
                "name": "Set webhook",
                "url": "/bot/set_webhook",
                "icon": "fas fa-sync-alt",
                "new_window": True,
            }
        ]
    },
    # https://fontawesome.com/v5.15/icons?d=gallery&p=2&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2&m=free
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "bot": "fas fa-robot",
        "bot.user": "fas fa-user-circle",
        "bot.message": "fas fa-comment-dots",
        "bot.funnyaction": "far fa-laugh-squint",
        "bot.bet": "fas fa-dice",
        "bot.notfoundanswer": "fas fa-question",
        "bot.startanswer": "fas fa-play",
        "bot.donate": "fas fa-donate",
        "bot.anekdot": "fas fa-grin-wink",
        "bot.status": "fas fa-link",
        "bot.demotivatortext": "far fa-square",
        "google_vision": "fab fa-google",
        "google_vision.request": "fas fa-globe",
        "google_vision.recognitiontype": "fas fa-eye",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": None,
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-lightblue",
    "accent": "accent-primary",
    "navbar": "navbar-lightblue navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
    "actions_sticky_top": False,
}
