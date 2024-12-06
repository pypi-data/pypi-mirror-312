import logging
import traceback

managers = set()


def emit(message):
    global managers
    try:
        for manager in managers:
            manager.publish(message)
    except Exception as e:
        logging.error(str(e))
        traceback.print_exception(e)