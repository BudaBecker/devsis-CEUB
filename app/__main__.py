from app.GUI.create_gui import CulinaryGUI
from app.server.server_api import CulinaryServer


def main():
    try:
        gui = CulinaryGUI()
        server = CulinaryServer.start_server()
        gui.run()

    except Exception as e:
        print(f"Error starting application: {e}")
        raise


if __name__ == "__main__":
    main()
