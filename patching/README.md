# Description

The code here shows how to patch a class in one module that has been imported by other module.

`the_module` module contains two sub-modules, `module_a.py` and `module_b.py`, and `module_b.py` imported the class `ModuleA` which is defined in `module_a.py`.

For unittest, we need to mock the `ModuleA` imported by `module_b.py`. How to do that?

# Mocking the Right Module

Since the class `ModuleA` is already been imported by `module_b.py`, we have to mocked out the `ModuleA` imported by `module_b.py`, instead of the `ModuleA` in `module_a.py`.
Please read the test code `tests/testModuleB.py` for details.

# References

[Patch Decorators: Where to patch](http://www.voidspace.org.uk/python/mock/patch.html#id1)
