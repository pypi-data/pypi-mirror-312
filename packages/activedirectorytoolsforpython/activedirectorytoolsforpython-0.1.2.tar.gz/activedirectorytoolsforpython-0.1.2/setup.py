from setuptools import setup, find_packages
import os
with open(os.path.join(os.path.dirname(__file__),"README.md")) as f:
    long_desc = f.read()
with open(os.path.join(os.path.dirname(__file__),"requirements.txt")) as f:
    dependencies = f.read().splitlines()

setup(
    name='activedirectorytoolsforpython',
    version='0.1.2',
    py_modules=["activedirectorytoolsforpython"],
    url='https://newgit.inuxnet.org/devel/activedirectorytoolsforpython',
    license='MIT',
    license_files = ('LICENSE.txt',),
    long_description=long_desc,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={
        "Documentation": "https://newgit.inuxnet.org/devel/activedirectorytoolsforpython",
        "Source Code": "https://newgit.inuxnet.org/devel/activedirectorytoolsforpython",
    },
    packages=find_packages(where="activedirectorytoolsforpython"),
    package_dir={'': 'activedirectorytoolsforpython'},
    include_package_data=True,
    install_requires=dependencies,
    author='Jess Williams',
    keywords="activedirectorytoolsforpython activedirectory ldap get-aduser powershell get-adgroup "
             "get-adorganizationalunit get-adobject",
    author_email='devel@inuxnet.org',
    description='Set of tools for Active Directory using python.',
    entry_points={"console_scripts": ["GetADObject=activedirectorytoolsforpython:main",
                                      "GetADUser=activedirectorytoolsforpython:main_getaduser",
                                      "GetADGroup=activedirectorytoolsforpython:main_getadgroup",
                                      "GetADComputer=activedirectorytoolsforpython:main_getadcomputer",
                                      "GetADOrganizationalUnit=activedirectorytoolsforpython"
                                      ":main_getadorganizationalunit"]},
)