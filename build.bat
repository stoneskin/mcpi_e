@echo off

echo install setuptools
py -m pip install --upgrade setuptools
echo install twine
py -m pip install --user --upgrade setuptools wheel
echo install twine
py -m pip install --user --upgrade twine
echo delete dist\*
del dist\* /q


echo build dist files
py setup.py sdist bdist_wheel

echo upload to pipy
py -m twine upload --repository pypi dist/*

pause

