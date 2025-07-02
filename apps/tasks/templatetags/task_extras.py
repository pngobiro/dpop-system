from django import template
from django.apps import apps

register = template.Library()

@register.filter
def instanceof(obj, model_name):
    """
    Returns True if the object is an instance of the given model name (string).
    Usage: {{ object|instanceof:"ModelName" }}
    """
    try:
        app_label, model_name = model_name.split('.')
        model = apps.get_model(app_label, model_name)
    except ValueError:
        # If no app_label is provided, assume it's in the same app as the object's model
        if hasattr(obj, '_meta'):
            app_label = obj._meta.app_label
            model = apps.get_model(app_label, model_name)
        else:
            return False # Cannot determine app_label
    except LookupError:
        return False # Model not found

    return isinstance(obj, model)