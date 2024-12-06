import atexit
import os
import sys

from make87.topics import TypedPublisher, get_publisher, resolve_topic_name
from make87_messages.text.log_message_pb2 import LogMessage


class _StdOutHandler:
    """Redirects stdout to a topic."""

    def __init__(self, topic):
        self._topic: TypedPublisher = topic
        self._original_stdout = sys.stdout

    def write(self, message):
        if self._topic is not None and message.strip():
            self.publish_log(message)
        self._original_stdout.write(message)

    def flush(self):
        pass

    def publish_log(self, message):
        log_msg = LogMessage()
        log_msg.timestamp.GetCurrentTime()
        log_msg.level = LogMessage.INFO
        log_msg.message = message
        log_msg.source = "stdout"
        log_msg.file_name = os.path.relpath(__file__, os.getcwd())
        log_msg.line_number = 0
        log_msg.process_id = os.getpid()
        log_msg.thread_id = 0
        self._topic.publish(message=log_msg)

    def restore_stdout(self):
        sys.stdout = self._original_stdout


def setup():
    """Sets up the stdout handler."""
    try:
        topic = get_publisher(name=resolve_topic_name("STDOUT"), message_type=LogMessage)
        stdout_handler = _StdOutHandler(topic)
        sys.stdout = stdout_handler
        atexit.register(stdout_handler.restore_stdout)
    except Exception as e:
        print(f"No stdout topic setup. Will not publish stdout. Error: {e}")


def cleanup():
    """Cleans up the stdout handler."""
    if isinstance(sys.stdout, _StdOutHandler):
        sys.stdout.flush()
        sys.stdout.restore_stdout()
