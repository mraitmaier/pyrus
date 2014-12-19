"""
    cli.py - script implementing a Cli class that is used to build apllication
             using CLI interface.

    NOTE: this is a module, so it is not meant to be used standalone, but to be
    imported.
"""
# HISTORY ######################################################################################################################
#
#   1   Aug10 MR The first working version of the script; limited testing performed, but seems to work fine.
#   2   Dec14 MR Ported to Py3
#
################################################################################################################################
NAME = "Command-line interface automatization"
VERSION = "2"
AUTHOR = "Miran R."

from command import Command, CommandList, CommandError

_HELPTEXT = """\
This command is used to display help. If command without arguments is used, all know commands are listed with
short description. If 'help <command-name> is issued, the complete info about the <command-name> is displayed.
"""

class Cli(object):
    """ """

    def __init__(self, prompt="> "):
        """Ctor"""
        self._prompt = prompt
        self._cmdlist = CommandList()
        self._cmdargs = ""
        self.__registerExit()
        self.__registerHelp()

    def __registerHelp(self):
        """Register CLI built-in 'help' command."""
        hlp = Command("help")
        hlp.registerCallback(self.__helpAction)
        hlp.setSyntax("help [all | <command-name> ]")
        hlp.setDescription("Display help text.")
        hlp.setHelp(_HELPTEXT)
        self.addCommand(hlp)

    def __helpAction(self, args):
        """Implemetation of the built-in 'help' command."""
        if len(args) > 0:
            if args[0] == "all":
                self._cmdlist.displayAll()
            else:    
                cmd = self._cmdlist.find(args[0])
                if cmd is not None:
                    cmd.displayHelp()
                else:
                    self._cmdlist.display()
        else:   
            self._cmdlist.display()

    def __registerExit(self):
        """Register CLI built-in 'exit' command."""
        exit = Command("exit")
        exit.setSyntax("exit")
        exit.setDescription("Exit the application")
        exit.setHelp("""\nThis command is used to exit the application.""")
        exit.registerCallback(self.__exitAction)
        self.addCommand(exit)

    def __exitAction(self, args):
        """Implemetation of the built-in 'exit' command."""
        print("Bye")
        raise SystemExit

    def __findCommand(self, cmdstr):
        """Find a command in command list using a string as input."""
        cmd = None
        args = ""
        cmdlist = cmdstr.split()
        if len(cmdlist) > 0:
            cmd = self._cmdlist.find(cmdlist[0]) 
            if len(cmdlist) > 1:
                args = cmdlist[1:]
        return (cmd, args)

    def getCommandArgs(self):
        """Returns the current command's arguments as a string."""
        return self._cmdargs

    def addCommand(self, cmd):
        """Append a new command to command list. """
        assert isinstance(cmd, Command) 
        self._cmdlist.append(cmd)

    def start(self):
        """Start the CLI itself. """
        print("%s v%s, (c) by %s" % (NAME, VERSION, AUTHOR))
        print("Try typing 'help' to start...")
        while True:
            cmdstr = "" # user input string
            # read the user input; catch ctrl-c and ignore it
            try:
                cmdstr = input(self._prompt)
            except KeyboardInterrupt:
                continue
            # if command string is empty, just go on looping
            if cmdstr.strip() == "":
                continue
            # find the command in registered commands' list
            (cmd, args) = self.__findCommand(cmdstr.strip())
            # save the command arguments for later, they might be needed...
            if cmd is not None:
                self._cmdargs = cmdstr.replace(cmd.getName(), " ", 1)
            else:
                self._cmdargs = ""
            # now, let's execute the command
            if cmd is not None:
                cmd.execute(args)
            else:
                print("Command '%s' not registered..." % cmdstr)
                continue

###################### testing...
def test():
    pass

if __name__ == "__main__":
    test()  
