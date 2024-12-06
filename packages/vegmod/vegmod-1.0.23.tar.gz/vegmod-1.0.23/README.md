# Packaging the project

https://packaging.python.org/en/latest/tutorials/packaging-projects/

python3 -m pip install --upgrade build
python3 -m build

Delete all old dist/* files from previous versions

python3 -m twine upload --repository pypi dist/*