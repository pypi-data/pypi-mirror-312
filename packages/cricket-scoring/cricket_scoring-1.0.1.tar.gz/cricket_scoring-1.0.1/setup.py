from setuptools import setup, find_packages

setup(
    name='cricket_scoring',
    version='1.0.1',
    description='A library for cricket scoring logic.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Radha Kantipudi',
    author_email='x23226391@student.ncirl.ie',
    url='https://github.com/Rad-99/cricket_scoring',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
