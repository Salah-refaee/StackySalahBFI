### build the package then install it with pip/3 ##

## build the package
pip install build      # be its installed
python -m build        # build the package
## install the package
pip install --force-reinstall dist/*.whl
## delete unneeded files
rm -rf build dist *.egg-info

## test
#sbfi --help
#sbfi --use-compressor --run test.bf
#printf "\n"
#sbfi --already-compressed --run .compressed_last.sbfi
#printf "\n"
#sbfi --command-line-interface