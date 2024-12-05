from setuptools import setup, find_packages
import shutil
import os

__package_name__ = "mytestpackage"
__version__ = "1.0.0"
__stage__ = "dev"               # use "dev" or "prod"
__package_description__ = "Description"

setup(
    name=__package_name__ + "-dev" if __stage__.lower() in {"dev", "development"} else __package_name__,
    packages=[__package_name__],
    package_dir={__package_name__: 'src'},
    include_package_data=True,
    version=__version__,
    install_requires=[],  # Dependencies, if any
    description=__package_description__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    url='https://github.com/pleonisci/scimodules',  # GitHub repo URL
    #url=f"https://github.com/pleonisci/{__package__name}",    
)

#for dir_name in ['build', 'dist', f"{__package_name__}.egg-info", f"{__package_name__}_dev.egg-info", '__pycache__']:
#    shutil.rmtree(dir_name, ignore_errors=True)
#for file_pattern in ['*.pyc', '*.pyo']:
#    for root, dirs, files in os.walk('.', topdown=False):
#        for name in files:
#            if name.endswith(file_pattern):
#                os.remove(os.path.join(root, name))