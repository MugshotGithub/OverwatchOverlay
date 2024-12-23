import threading
from WebApp import app as flask_app
from waitress import serve
import GUI


def run_flask():
    serve(flask_app, host='127.0.0.1', port=5000)

def start_gui_thread():
    app = GUI.App()
    app.mainloop()

def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start GUI in the main thread
    start_gui_thread()

if __name__ == "__main__":
    main()