from setuptools import setup, find_packages

setup(
    name='pyfilemaster',  # Package name
    version='0.1.8',  # Initial release version
    author='beingshubh (Shubhashish Chakraborty)',  # Author name
    author_email='shubhashish147@gmail.com',  # Author email
    description='A Python package for file handling utilities',  # Short description
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',  # Description content type
    url='https://github.com/Shubhashish-Chakraborty/pyfilemaster',  # GitHub repository
    packages=find_packages(),  # Automatically find all packages
    include_package_data=True,  # Include non-code files (like LICENSE)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
    install_requires=[],  # e.g., ['pandas>=1.0']
    keywords='pyfilemaster , pyfilemaster pypi , pyfilemaster github, file handling, binary to CSV, binary , csv , text , excel , dat, file conversion , pyfilemaster python, pyfilemaster python package',  # Keywords for PyPI search
    license="MIT",  # Specify license
)
