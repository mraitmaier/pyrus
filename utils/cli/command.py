"""
    command.py -
"""

class Command(object):
    """
    Command - class representing CLI command

    This class has the following properties:
        name   - name of the command, of course
        syntax - syntax of the command
        desc   - short description of the command
        help   - longer description of the command, used primarily for help 
        action - callback function that actually implements the command
        hidden - flag that hides the command from being visible - such a
                 command should be used for testing or debugging purposes
    """
    def __init__(self, name, syntax='', desc='', help='', action=None, 
                             hidden=False):
        self._name = name
        self._syntax = syntax
        self._desc = desc
        self._help = help
        self._action = action
        self._hidden = hidden
    def getName(self):
        """Returns the name of the command."""
        return self._name
# NOTE: we don't define the 'set' method for command's name, since we don't
#       allow changing its name dynamically.  
    def getSyntax(self):
        """Sets the command syntax"""
        return self._syntax
    def setSyntax(self, s):
        """Returns the commands syntax"""
        self._syntax = s
    def getDescription(self):
        """Sets the command description"""
        return self._desc
    def setDescription(self, desc):   
        """Returns the commands description"""
        self._desc = desc
    def getHelp(self):
        """Sets the command help text"""
        return self._help
    def setHelp(self, help):
        """Returns the commands help text"""
        self._help = help
    def hide(self):
        """Sets the hidden parameter."""
        self._hidden = True
    def isHidden(self):
        """returns the value of 'hidden' parameter."""
        return self._hidden
    def registerCallback(self, action):
        """Register callback function that implements the command."""
        self._action = action
    def execute(self, args):
        """Execute callback and therefore execute the command itself."""
        rc = self._action(args)
        return rc
    def displayHelp(self):
        """
        Displays the complete information about the command. 
        Can be used for 'help' command implementation.
        """
        print 
        print 'COMMAND:' 
        print '\t', self._name
        print
        print 'DESCRIPTION:'
        print '\t', self._desc
        print
        print 'SYNTAX:' 
        print '\t%s' % self._syntax
        print
        print 'HELP:'
        print self._help
        print
    def displayShortInfo(self):
        """Displays short - one line - help info."""
        if self.isHidden():
            print '*%8s - %s' % (self._name, self._desc)
        else:
            print ' %8s - %s' % (self._name, self._desc)
    def checkSyntax(self):   
        """Checks the commands syntax."""
        print "Checking syntax not implemented yet."

class CommandList(list):
    """
    CommandList - class representing list of commands

    It is inherited from list class and therefore uses all of its methods.

    Adds the following methods to those inherited from list class:

    display    - displays a list of all commands that are not marked hidden
    displayAll - displays a list of all commands, including hidden ones
    find       - searches for a command with a given name
    """
    def __init__(self):
        super(CommandList, self).__init__()
    def display(self):
        """Displays short information for all commands in the list that
        are not hidden."""
        for cmd in self:
            if not cmd.isHidden():
                cmd.displayShortInfo()
        print
    def displayAll(self):
        """Displays short information for all commands in the list."""
        for cmd in self:
            cmd.displayShortInfo()
        print
    def find(self, name):
        """
        Searches the list of commands and tries to find the match
        according to given name. Returns the command found. If not found, 
        returns None.
        """
        for cmd in self:
            if cmd.getName() == name:
                return cmd
        return None       
    def append(self, item):
        #assert isinstance(item, Command)
        super(CommandList, self).append(item)

class CommandError(Exception):
    """Defines exception when working with commands."""
    default = 'Command Error'
    def __init__(self, msg = default):
        self._msg = msg
    def __str__(self):
        return self._msg

#*****************************************************************
#* Helper function
#*
def test():
    print 'Standalone execution'
    print __doc__
    print

    tst = Command('test')
    hlp = Command('help')

    l = CommandList()
    l.append(tst)
    l.append(hlp)
    l.display()

if __name__ == '__main__':
    test()
