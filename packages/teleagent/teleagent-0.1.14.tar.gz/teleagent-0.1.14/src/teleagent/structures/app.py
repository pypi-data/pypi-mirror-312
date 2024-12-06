from dataclasses import dataclass


@dataclass
class AppData:
    device_model: str
    system_version: str
    app_version: str
    lang_code: str
    system_lang_code: str
    lang_pack: str
