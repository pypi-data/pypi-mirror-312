from .configs.main_hub import main_hub
from .update import check_update


def run():
    check_update()
    main_hub()
