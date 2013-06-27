import os
from distutils.core import setup
from setuptools import find_packages


VERSION = __import__("blog").VERSION

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]

install_requires = [
]

# taken from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('blog'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[9:] # Strip "blogbase/" or "blogbase\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


setup(
    name="cotidia-blog",
    description="Blog extension for Cotidia CMSBase",
    version=VERSION,
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://bitbucket.org/guillaumepiot/cotidia-blog",
    download_url="https://bitbucket.org/guillaumepiot/cotidia-blog-base/downloads/cotidia-blog-%s.tar.gz" % VERSION,
    package_dir={'blog': 'blog'},
    packages=packages,
    package_data={'blog': data_files},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)
