import warnings

def warn_on_import():
    warnings.warn(
        "The lsdir package is designed to be run as a command-line tool, not imported as a module. "
        "If you need the functionality in your Python code, consider using the standard library's "
        "os.walk() or pathlib instead.",
        ImportWarning
    )

warn_on_import()
