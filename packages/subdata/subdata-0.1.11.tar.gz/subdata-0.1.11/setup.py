from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='subdata',  # Replace with your package’s name
    version='0.1.11',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ # List your dependencies here
        'pandas',
        'numpy',
        'huggingface_hub',
        'pyarrow',
        # 'fastparquet'
    ],
    url = 'https://github.com/frohleon/subdata_library',
    author='Leon Fröhling',  
    author_email='leon.froehling@gesis.org',
    description='A library for automatically creating targeted hate speech datasets.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',

)
