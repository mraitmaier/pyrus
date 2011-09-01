"""
singleton.py

This file contains an implementation of the Singleton pattern.
"""

class Singleton(object):
    """ @brief The Singleton class.
        @remarks Derived your classes from this one to make them a Singleton.
        In derived classes do NOT implement the __init__ Method, but instead the
        Init.
    """

    def __init__(self, *args, **kwargs):
        """ @brief Initializer.
            @remarks Do not implement this in derived classes.
        """
        if not '_instance_created' in self.__dict__:
            self.init(*args, **kwargs)
            self._instance_created = True

    def init(self, *args, **kwargs):
        """ @brief The Initializer Method.
            @param args [in]Arguments to this method.
            @param kwargs [in] Keyword arguments to this method.
            @exception NotImplementedError
            @remarks This method is only called once.
        """
        pass

    def __new__(class_, *args, **kwargs):
        """ @brief Method for creating the instance.
            @param args [in] Arguments to __init__.
            @param kwargs [in] Named arguments passed to init
            @remarks If you override this method in derived classes do
            not forget to call it from super class.
        """
        if not '_the_instance' in class_.__dict__:
            class_._the_instance = object.__new__(class_)
        return class_._the_instance

# TESTING ####################################################################

class Test(object):

    def __init__(self, a):
        self._a = a

    @property
    def a(self):
        return self._a

class SingletonTest(Test, Singleton):
    pass

def runtests():
    x = SingletonTest(10)
    print("Initial: " + str(x.a))
    print(str(x))
    print("###########################")
    y = SingletonTest(33)
    print("Second: " + str(x.a))
    print(str(x))
    print("###########################")
    y = SingletonTest(666)
    print("Third: " + str(x.a))
    print(str(x))

if __name__ == "__main__":
    print(__doc__)
    runtests()
