from interpreter import SNOLInterpreter

def main():
    """
    Entry point for the SNOL Interpreter application.
    Initializes and starts the interpreter session.
    """
    snol = SNOLInterpreter()
    snol.start()

if __name__ == "__main__":
    main()
