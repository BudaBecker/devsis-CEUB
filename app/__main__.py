from app.gui.create_gui import CulinaryGUI


def main():
    try:
        # Start GUI & DB
        # db = Database()
        # db.create_tables()
        
        # Start GUI
        gui = CulinaryGUI()
        gui.run()

    except Exception as e:
        print(f"Error starting application: {e}")
        raise


if __name__ == "__main__":
    main()
