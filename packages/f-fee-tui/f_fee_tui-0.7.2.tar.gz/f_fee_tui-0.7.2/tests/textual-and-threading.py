"""
This gist is a stand alone Textual App intended to show how to handle Threading in a Textual App, especially when
the code in the thread `run()` method would crash or raise an Exception. It also demonstrates how messages shall be
posted to either the App or the Screen depending on where the receiving method is implemented.

There are two Messages, `RuntimeErrorCaught` and `ThreadCrashed`. Both messages are sent from the Thread, the former
will be sent to the App, the latter needs to be sent to the 'master' Screen. That is because the receiving methods are
implemented in the App and in the 'master' screen respectively.

This gist is mainly written as a reminder to myself for future use, but I hope it will be useful to other Textual users.
"""
import datetime
import random
import threading
import time
from queue import Queue

from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import RichLog
from textual.widgets import Static


class RuntimeErrorCaught(Message):
    """A Message that is sent to the App."""
    def __init__(self, message: str, exc: Exception):
        super().__init__()
        self.msg = message
        self.exc = exc


class ThreadCrashed(Message):
    """A Message that is sent to the MasterScreen."""
    def __init__(self, message: str, exc: Exception):
        super().__init__()
        self.msg = message
        self.exc = exc


class Command(threading.Thread):
    """
    A thread that is used to execute commands on services in the background and report back to the App with
    posted messages. Commands are passed using the thread-safe Queue.
    """
    def __init__(self, app: App, command_q: Queue):
        super().__init__()
        self._app = app
        self._command_q = command_q
        self._cancelled = threading.Event()

    def run(self):
        self._app.log("Command thread started ...")

        while True:
            if self._cancelled.is_set():
                break

            try:
                # Within this try ... except: clause, you would execute your code which might connect to some
                # services, execute complex commands it gets from the command queue and might raise an exception.
                # The code snippet below simulates an Exception that is thrown after some time.

                if random.random() < 0.1:
                    raise RuntimeError("A fake runtime error.")

            except RuntimeError as exc:
                msg = "We got a RuntimeError in the Command thread ..."
                self._app.get_screen("master").post_message(ThreadCrashed(msg, exc))
                self._app.post_message(RuntimeErrorCaught(msg, exc))

                if self.sleep_or_break():
                    break

                self._app.notify("Re-activating Command Thread after 10.0s")

    def sleep_or_break(self) -> bool:
        """
        Sleep for 10 seconds. If the thread was cancelled, break early and return True.
        """
        for _ in range(100):
            if self._cancelled.is_set():
                is_cancelled = True
                break
            time.sleep(0.1)
        else:
            is_cancelled = False

        return True if is_cancelled else False

    def cancel(self) -> None:
        self._cancelled.set()


class MasterScreen(Screen):

    DEFAULT_CSS = """
    #lbl-msg {
        width: auto;
        padding: 1 2;
        border: wide white;
    }
    """

    def __init__(self):
        super().__init__()
        self._command_q = Queue()
        self._commanding_thread = Command(self.app, self._command_q)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        with Vertical():
            yield Static("Gist for demonstrating how threading works with Textual.", id="lbl-msg")
            yield RichLog(max_lines=200, markup=True, id="rich-log")

    def on_mount(self) -> None:
        self._commanding_thread.start()

    def on_unmount(self) -> None:
        self._commanding_thread.cancel()

        if self._commanding_thread.is_alive():
            self._commanding_thread.join()

    def on_thread_crashed(self, message: ThreadCrashed):
        self.log(f"MasterScreen: {message.msg}: {message.exc}")
        self.query_one("#rich-log", RichLog).write(f"{datetime.datetime.now():%X} [green]MasterScreen:[/] {message.msg} — {message.exc}")


class ThreadApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    SCREENS = {"master": MasterScreen}

    def on_mount(self):
        self.push_screen("master")

    def on_runtime_error_caught(self, message: RuntimeErrorCaught):
        self.log(f"App: {message.msg}: {message.exc}")
        self.query_one("#rich-log", RichLog).write(f"{datetime.datetime.now():%X} [red]App:[/] {message.msg} — {message.exc}")


if __name__ == '__main__':

    app = ThreadApp()
    app.run()
