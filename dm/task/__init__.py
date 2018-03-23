import logging
import signal


def on_task_terminal(running):

    def signal_received(signum, _):
        logging.info('signal received: %s', signum)
        running.clear()

    signal.signal(signal.SIGTERM, signal_received)
    signal.signal(signal.SIGINT, signal_received)
    if hasattr(signal, 'SIGQUIT'):
        signal.signal(signal.SIGQUIT, signal_received)