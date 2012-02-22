#!/usr/bin/env python

from setuptools import setup, find_packages
import inviter

setup(
    name='django-inviter',
    version=inviter.__version__,
    description='Invite users to your Django apps',
    long_description=open('README.rst').read(),
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=[
        "shortuuid >= 0.1",
    ],
    include_package_data=True,
    zip_safe=False,
)
