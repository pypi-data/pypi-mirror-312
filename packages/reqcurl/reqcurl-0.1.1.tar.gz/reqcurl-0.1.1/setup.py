from setuptools import setup, find_packages

setup(
    name='reqcurl',  # Name of the package
    version='0.1.1',  # Version number
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[  # Dependencies
        'requests',  # If you depend on any third-party libraries
    ],
    tests_require=[  # Testing dependencies
        'pytest',
    ],
    test_suite='tests',  # Test suite location
    author='Sufiyan Ali Iqbal',
    author_email='sufiyanaliiqbal@gmail.com',
    description='A Python wrapper for cURL commands to execute API requests.',
    long_description=open('README.md', encoding='utf-8').read(),  # Read from README.md for long description
    long_description_content_type='text/markdown',  # Specify markdown for the long description
    url='https://github.com/yourusername/reqcurl',  # URL for the project, e.g., GitHub
    classifiers=[  # PyPI classifiers for the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify supported Python versions
)
