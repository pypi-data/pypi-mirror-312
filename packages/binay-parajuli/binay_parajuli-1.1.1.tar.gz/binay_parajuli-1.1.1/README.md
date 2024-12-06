# Building and uploading python package in PyPI

Install -> setupttools, twine and wheel

1.Create package_dir with  __init__.py and modules inside it.
Also, add setup.py and can also add README.md and LICENSE.txt as optional 

2.Then build with python3 setup.py sdist bdist_wheel 
which returns binay_parajuli.egg-info , build and dist folders

3.Upload using twine upload dist/*


View at: https://pypi.org/project/binay-parajuli/0.0.1/


