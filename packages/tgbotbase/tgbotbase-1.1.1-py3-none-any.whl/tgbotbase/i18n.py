import os

import i18n as annotation_i18n

from tgbotbase.utils import SHARED_OBJECTS, logger, utils_settings

i18n: annotation_i18n = SHARED_OBJECTS.get("i18n")

if i18n is None:
    logger.warning(
        "i18n is not initialized to SHARED_OBJECTS, import i18n and add as value to key 'i18n' to SHARED_OBJECTS"
    )

# load locales
i18n.load_path.append(
    os.path.join(os.path.dirname(__file__), utils_settings["locales_folder"])
)
i18n.set("encoding", "utf-8")


def localizator(key: str, locale: str = "en", **kwargs) -> str:
    return i18n.t(
        f"{utils_settings['locales_startswith']}.{key}", locale=locale, **kwargs
    )


def reload_i18n() -> None:
    i18n.translations.container.clear()

    for dir in i18n.load_path:
        i18n.resource_loader.load_directory(dir)
