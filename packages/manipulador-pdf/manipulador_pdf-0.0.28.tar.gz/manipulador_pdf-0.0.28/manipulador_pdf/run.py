from .configs.main_hub import main_hub
from manipulador_pdf.configs.update import check_update


def run():
    check_update()
    main_hub()
