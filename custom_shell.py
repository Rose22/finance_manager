import config
import sys

class BaseShell(object):
    """The class that all shells can extend from"""

    def input_type(self, type, prompt = ">"):
        finished = False
        while not finished:
            # Try and ask for a value
            value = raw_input(prompt + " ")

            if not value:
                return

            # If the value is not of the specified type, notify the user and prompt again.
            try:
                if type == "int":
                    value = int(value)
                    finished = True
                elif type == "float":
                    value = float(value)
                    finished = True
                elif type == "day":
                    value = int(value)

                    if value > 31:
                        print "There are a maximum of 31 days"
                    else:
                        finished = True
                elif type == "search":
                    if value not in ['day', 'category', 'name', 'price']:
                        print "Invalid search type"
                    else:
                        finished = True
                elif type == "string":
                    finished = True
                    pass
                else:
                    raise ValueError("This type is not supported by prompt_type")
            except:
                print "Invalid input"

        return value

class GenericShell(BaseShell):
    """The Generic Shell. This is the shell you would normally subclass from.

    It has a few flags you can use:
        - main_shell is a variable that determines whether or not this is the main loop. If this is set to True, the shell will accept command-line arguments when those are given, instead of starting in interactive mode.
        - prompt is a string that determines what the prompt text is

    The concept works via methods that you add to the subclass. Please look at the documentation for the methods within this GenericShell.
    """

    main_shell = False
    prompt  = "Shell> "
    cmd_associations = {}

    __running = False

    def intro(self):
        """This method runs at the beginning of the command loop"""

        pass

    def pre_prompt(self):
        """This method runs every time before the prompt appears"""

        pass

    def run_loop(self):
        """This is the main loop of the GenericShell.

        It runs while self.running is True (set it to False to abort the loop)
        It uses self.interpret_cmd() to interpret the commands.
        For information on how to add commands, see self.interpret_cmd()
        """

        # If this is flagged as a main shell, support direct command line interaction via sys.argv
        if self.main_shell and len(sys.argv) > 1:
            self.interpret_cmd(" ".join(sys.argv[1:]))
            return

        # Show the introduction upon first start of the loop
        self.intro()

        self.__running = True
        while self.__running:
            # Run this every time before showing the prompt
            self.pre_prompt()

            # Prompt for and interpret the input
            cmd = raw_input(self.prompt+" ")
            self.interpret_cmd(cmd)

            print

    def stop_loop(self):
        """Stops the loop"""

        self.__running = False
        return

    def interpret_cmd(self, cmd):
        """This method will run through a dict and run the associated method with each key.
        When you type the key into the prompt, the method gets executed.

        The dict is called self.cmd_associations, and it is set up somewhat like this, for example:
        self.cmd_associations = {
            "help":     self.cmd_help,
            "h":        self.cmd_help,
            "?":        self.cmd_help,

            "greet":    self.cmd_greet
        }

        In this case, typing either help, h, or ? into the command prompt would execute self.cmd_help()
        And typing greet would run self.cmd_greet()

        You can setup self.cmd_associations in the constructor of your subclass.
        """
        if cmd in self.cmd_associations:
            self.cmd_associations[cmd]()
        elif not cmd:
            pass
        else:
            print "Unknown command."
