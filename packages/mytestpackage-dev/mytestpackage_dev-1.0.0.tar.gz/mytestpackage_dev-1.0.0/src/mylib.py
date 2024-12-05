class MyClass():
    """
    This is an template or example Class. SCI uses the Pascal naming convention for classes and for the source files.

    Each file should either contain 1 class or multiple methods. Do not combine both.
    """
    def __init__(self):
        pass
    def my_class_method(self):
        """
        For methods we use the snake case convention. This method just prints a welcome statement
        """
        print("hello SCI to the world")

def my_def(a=0):
    """
    This is a little method that takes a number and adds 1
    """
    return a+1