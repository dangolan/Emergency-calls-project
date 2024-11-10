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
            
            # Check if the response code is 200
            if res.status_code != 200:
                self.error_signal.emit(f"Error: Received status code {res.status_code}")
            else:
                # Attempt to parse the response as JSON
                try:
                    data = res.json()  # Parse JSON content
                    self.result_signal.emit(data)
                except ValueError:
                    # Fallback to raw text if JSON parsing fails
                    self.result_signal.emit(res.text)
                    
        except Exception as e:
            # Emit an error signal with the exception message
            self.error_signal.emit(f"Exception: {str(e)}")
