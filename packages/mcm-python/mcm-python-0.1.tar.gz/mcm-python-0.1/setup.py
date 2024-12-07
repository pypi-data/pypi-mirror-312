from setuptools import setup, find_packages

setup(
    name='mcm-python',  # Name of your package (change it to match your package name)
    version='0.1',  # Version number of your package
    packages=find_packages(),  # Automatically find packages in the current directory
    install_requires=[],  # List of dependencies (empty for now, add them if needed)
    author='Ariyan',
    author_email='ariyan@mycountrymobile.com',
    description='A simple Python package for My Country Mobile',
    long_description=open('README.md').read(),  # Read the content of README.md
    long_description_content_type='text/markdown',  # Indicates the type of the long description
    url='https://github.com/Mycountrymobile-com/mcm-python/',  # Replace with your actual GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',  # Compatible with Python 3
        'License :: OSI Approved :: MIT License',  # License used for the package
        'Operating System :: OS Independent',  # Works on any OS
    ],
)
