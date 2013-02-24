from socketio.namespace import BaseNamespace
import queue
import logging
logger = logging.getLogger("app.namespace")


class Requests(BaseNamespace):

    def initialize(self):
        logger.debug('adding a queue listener.')
        queue.add_listener(self.new_request)
        super(Requests, self).initialize()

    def disconnect(self, *args, **kwargs):
        logger.debug('removing a queue listener due to client disconnection.')
        queue.remove_listener(self.new_request)
        super(Requests, self).disconnect(*args, **kwargs)

    def on_new_client(self):
        logger.info("new connection established.")

    def new_request(self, request):
        """Server triggered event to send a new request."""
        logger.debug('emitting "new requets" for %s' % self.socket.sessid)
        self.emit('new request', request.serialize())
