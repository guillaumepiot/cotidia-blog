from setuptools import find_packages, setup


setup(
    name="cotidia-blog",
    description="Blog for Cotidia base project.",
    version="1.0",
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/blog/",
    packages=find_packages(),
    package_dir={'blog': 'blog'},
    package_data={
        'cotidia.cms': [
            'templates/admin/blog/*.html',
            'templates/admin/blog/includes/*.html',
            'templates/blog/*.html',
            'templates/blog/includes/*.html',
            'templates/blog/notice/*.html',
            'templates/blog/notice/*.txt',
        ]
    },
    namespace_packages=['cotidia'],
    include_package_data=True,
    install_requires=[
        'pytz',
        'django-datetime-widget==0.6',
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
