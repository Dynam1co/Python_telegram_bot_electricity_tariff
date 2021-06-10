import config as cfg


def get_telegram_token():
    return cfg.TELEGRAM_TOKEN


def get_telegram_group_id():
    return cfg.TELEGRAM_GROUP_ID


def get_source() -> str:
    return cfg.SOURCE


def get_red_circle() -> str:
    return cfg.RED_CIRCLE


def get_green_circle() -> str:
    return cfg.GREEN_CIRCLE