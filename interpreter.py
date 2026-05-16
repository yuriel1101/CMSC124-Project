from command_handler import run_command

class SNOLInterpreter:
    """
    Main controller class for the SNOL interpreter.
    Maintains the state of the symbol table and the execution loop.
    """
    def __init__(self):
        # Stores variables and their corresponding numeric values
        self.symbol_table = {}
        # Flag to control the interpreter's main loop
        self.running = True

    def start(self):
        """
        Activates the interactive SNOL environment.
        Continuously prompts the user for commands until terminated.
        """
        print("The SNOL environment is now active, you may proceed with giving your commands.\n")
        while self.running:
            try:
                line = input("Command: ").strip()
                if not line:
                    continue
                # Delegates command execution to the command handler module
                run_command(self, line)
            except (EOFError, KeyboardInterrupt):
                # Gracefully handles termination via keyboard interrupts
                print("\nInterpreter is now terminated...")
                break
