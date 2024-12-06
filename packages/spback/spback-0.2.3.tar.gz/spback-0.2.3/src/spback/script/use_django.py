import os


def use_django(conf_path="conf.settings"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", conf_path)
    import django

    django.setup()
