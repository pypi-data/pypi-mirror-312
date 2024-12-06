import json
import atexit

# Load the compiled library
try:
    from .sdk_python3 import *
    atexit.register(unload)

    __version__ = import_version

    info = json.loads(import_info_str)

except ModuleNotFoundError as e:
    # TODO Use ImportError or ModuleNotFoundError ?
    # TODO Show this only if it concerns an ABI issue

    import os

    modulename = os.path.basename(os.path.dirname(__file__))

    print(f"Failed to import {modulename}: {e}")

    import sysconfig
    import glob
    import platform
    import re

    def get_os_details(abi):
        version = 'unknown version'
        arch = 'unknown arch'
        os = 'unknown os'
        try:
            res = re.search(r'cpython-([^-]+)-([^-]+)-(.+)', abi)

            version = res.group(1)
            version = version[:1]+'.'+version[1:]

            arch = res.group(2)
            osname = res.group(3)
        except:
            # Can't block the information if this fails
            pass

        return f"Python {version}, Arch:{arch}, OS:{osname}"

    abi_current = sysconfig.get_config_var('SOABI')
    print(f"The version of the running python interpreter is {get_os_details(abi_current)} (ABI: {abi_current})")

    print(f"whereas this {modulename} module offers the versions:")
    for libfilepath in glob.glob(os.path.dirname(__file__)+'/*.so'):
        libfilename = os.path.basename(libfilepath)
        abi_available = libfilename[len('sdk_python3.'):-len('.so')]
        print(f"    {get_os_details(abi_available)} (ABI: {abi_available})")

    print(f"It is very likely that this {modulename} module has been compiled for a different Python version, architecture or operating system.")

    raise e
