import gevent
import logging
logger = logging.getLogger("app.queue")


POLLING_PERIOD = 0.05
__queue = []
__listeners = []


def add_listener(listener):
    logger.debug('adding a listener.')
    __listeners.append(listener)


def remove_listener(listener):
    logger.debug('removing a listener.')
    __listeners.remove(listener)


def put(entry):
    logger.debug("putting to the queue.")
    __queue.insert(0, entry)


def _poll_the_queue(polling_period=POLLING_PERIOD):
    while True:
        while __queue:
            logger.debug('queue is not empty.')
            entry = __queue.pop()
            for listener in __listeners:
                logger.debug('calling a listener.')
                listener(entry)
        gevent.sleep(polling_period)


logger.info('spawning the poller for the queue.')
__poller = gevent.spawn(_poll_the_queue)
