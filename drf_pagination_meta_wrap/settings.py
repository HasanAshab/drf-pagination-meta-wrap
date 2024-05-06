from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver


class PackageSettings:
    setting_name = "DRF_PAGINATION_META_WRAP"

    def __init__(
        self,
        defaults=None,
    ):
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, self.setting_name, {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self) -> None:
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


DEFAULTS = {
    "PAGINATED_RESPONSE_META_KEY": "meta",
    "PAGINATED_RESPONSE_DATA_KEY": "results",
}

package_settings = PackageSettings(DEFAULTS)


@receiver(setting_changed)
def reload_package_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == package_settings.setting_name:
        package_settings.reload()
