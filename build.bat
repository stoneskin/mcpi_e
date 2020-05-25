
@echo off

py -m pip install --upgrade setuptools
py -m pip install --user --upgrade setuptools wheel
py -m pip install --user --upgrade twine

del dist\* /q
py setup.py sdist bdist_wheel
py -m twine upload --repository pypi dist/*

pause

