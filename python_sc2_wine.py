"""
Setup python-sc2 on a linux machine which already has a working SC2 installation under wine.

Tips:
Kill/exit any already running Battle.net.exe or SC2.exe before launching.
"""
import os
from sc2 import paths as sc2_paths

SC2PATH = os.environ.get('SC2PATH', '~/.wine/drive_c/Program Files/StarCraft II')
SC2EXE_NAME = os.environ.get('SC2EXE', 'SC2.exe')

# The executable name the python-sc2 will look for inside <SC2PATH>/Versions/BaseXXXX/:
BINPATH = sc2_paths.BINPATH[sc2_paths.PF]


def generate_proxy_scripts():
    def create_script(dir_path):
        file_path = os.path.join(dir_path, BINPATH)
        with open(file_path, 'w') as script:
            script.write((
            """#!/bin/sh
            # Create a temporary batch script
            batfile=$(mktemp /tmp/sc2_XXXX.bat)
            startdir=$(winepath -w "%s")
            echo "cd /d  \\"$startdir\\"">>$batfile
            expath=$(winepath -w "%s/%s")
            echo "\\"$expath\\" %%*">>$batfile
            cat $batfile
            wineconsole "$(winepath -w "$batfile")" "$@"
            rm "$batfile"
            """ % (
                    working_directory_for_sc2_exe,
                    dir_path,
                    SC2EXE_NAME,
                )).replace('    ', '')  # replace formatting spaces from code formatting
                         )
        # Set as executable
        os.chmod(file_path, 0o754)

    sc2_path = os.path.expanduser(SC2PATH)
    working_directory_for_sc2_exe = os.path.join(sc2_path, 'Support')  # The windows exe should be started from here.
    # Version dir contains dirs in the form BaseXXXX(where x is version)
    # and SC2 exe files inside each of 'em which is the ACTUAL sc2 client.
    # sc2 lib chooses one(probably latest) from it and runs the file with name BINPATH(from sc2/paths.py)
    # found inside the BaseXXXX dir.
    # For Linux platform, BINPATH is set to SC2_x64,
    # while for windows it is SC2_x64.exe/SC2.exe depending on architecture.

    # Here for every version, an executable shell script is created in place of the expected binary
    # that when invoked with arguments, will propagate them to the windows exe through wine.
    versions_directory_root_path = os.path.join(sc2_path, 'Versions')

    for a_version in os.listdir(versions_directory_root_path):
        full_path = os.path.join(versions_directory_root_path, a_version)
        if os.path.isdir(full_path):
            if str(os.path.split(a_version)[1])[:4] == 'Base':
                create_script(full_path)
