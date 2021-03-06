import os
from setuptools import setup, find_packages
import sulci


try:
    reqs = open(os.path.join(os.path.dirname(__file__),
                             'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''


setup(
    name='sulci',
    version=sulci.get_version(),
    description=
    'French textmining tool based on Liberation corpus and thesaurus',
    author='Yohan Boniface',
    author_email='y.boniface@liberation.fr',
    url='https://github.com/yohanboniface/sulci',
    packages=find_packages(),
    include_package_data=True,
    package_data={'sulci': ['corpus/*','templates/sulci/*']},
    install_requires=reqs,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
