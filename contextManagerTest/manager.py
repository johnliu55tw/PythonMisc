class Manager(object):

    def __init__(self, *args, **kwargs):
        """The constructor for direct call.

        If the Manager class is directly call and instantiated, like:

        >>> context = Manager(arg1, arg2)
        >>> assert isinstance(context, Manager)

        This method will be called, contructs the instance by the given
        arguments and return the object itself. With this method, the Manage
        could behave just like normal class.
        """
        print("__init__ called.")

    def __enter__(self):
        """The method for the with statement.

        When this class is used in a with statement, several things will
        happened:

        >>> with Manager(arg1, arg2) as context:
        >>>     pass

        First, the arguments 'arg1' and 'arg2' will be passed to __init__ and
        calls it, instantiate the object. Thus this method takes no arguments.

        Second, this __enter__ method will be called. The return value of this
        method will be assigned to the variable the comes after the 'as'
        keyword. Usually this method returns self.

        Third and the most important one, if an exception is raised within this
        method, before the return could happened, the __exit__ method, which
        suppose to handle this situation, will NOT be called. You have to
        either assure that no exception will be raised within this method, or
        handle internall errors manually, like calling the necessary close()
        method to some of the internal objects, or do some clean ups.
        """
        print("__enter__ called")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """The method for the with statement.

        This method will be called if the with statement block is finished, or
        an exception is raised within the with statement. For example:

        >>> with Manager(arg1, arg2) as context:
        >>>     raise ValueError("ERR")

        This method will be called, and the exception that got raised, which is
        ValueError("ERR") in this case, will be passed to this method.

        Noted that this method could decides whether the exception should be
        suppressed by returning a true value. If this method returns a false
        value, the exception will be propagated to the user.

        """
        print("__exit__ called")
        self.cleanUp()

    def cleanUp(self):
        print("clean up called.")

    def raisedMethod(self):
        print("raisedMethod called.")
        raise RuntimeError("Err in raisedMethod")
