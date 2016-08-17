import sys

class BaseShell():
    def input_type(self, type, prompt = ">"):
        finished = False
        while not finished:
            value = raw_input(prompt + " ")

            if not value:
                return

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
    main_shell = False
    prompt  = "Shell> "
    intro   = ""

    def __init__(self):
        self.cmd_associations = {}

    def run_loop(self):
        if self.main_shell and len(sys.argv) > 1:
            self.interpret_cmd(" ".join(sys.argv[1:]))
            return

        print self.intro

        while True:
            print self.prompt,
            cmd = raw_input()

            self.interpret_cmd(cmd)

            print

    def interpret_cmd(self, cmd):
        if cmd in self.cmd_associations:
            self.cmd_associations[cmd]()
        else:
            print "Unknown command."
