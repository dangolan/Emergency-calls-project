from PySide6.QtCore import Signal, QObject
from threading import Thread

class Worker(QObject):
    # Signals to communicate results and errors back to the main thread
    result_signal = Signal(object)  # Signal to send the result back
    error_signal = Signal(str)      # Signal to send error messages back

    def __init__(self, func, parent=None):
        super().__init__(parent)
        self.func = func

    def start(self):
        # Create and start the worker thread
        thread = Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):
        try:
            # Call the provided function and get the response object
            res = self.func()
            if res:
                # Emit the result signal with the response object
                self.result_signal.emit(res)
            else:
                # Emit an error signal with a message
                self.error_signal.emit("No data found")
                    
        except Exception as e:
            # Emit an error signal with the exception message
            self.error_signal.emit(f"Exception: {str(e)}")
