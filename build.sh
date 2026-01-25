printf "Building SBFI...\n"
python -c "import os
try:
    import build
    del build # no need, just checking if its installed
    print('\"build\" installed')
except Exception:
    print('installing \"build\"...')
    os.system('pip install build')"

rm -rf dist *.egg-info # those are from the previous build, remove them if they exist
python -m build
python -c "
import os
installed = False
try:
    import sbfi
    del sbfi # no need, just checking if its installed
    installed = True
except Exception:
    pass
if installed:
    print('SBFI already installed with version: ' + __import__('sbfi').VERSION)
    print('Upgrading SBFI...')
    os.system('pip install --upgrade')
"