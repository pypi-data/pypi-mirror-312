# setup.py
from setuptools import setup, find_packages

setup(
    name='gns_helper',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'Flask',                    # Web framework
        'Flask-JWT-Extended',       # JWT-based authentication
        'Pillow==9.5.0',            # Image processing (barcodes, labels)
        'pymysql',                  # MySQL database connector
        'dbutils',                  # Database connection pooling
        'pyyaml',                   # YAML parsing for configuration
        'requests',                 # HTTP requests for APIs (if needed)
    ],
    include_package_data=True,
    description='A package for common GNS functions',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # Specify markdown format
    author='Komal Swami',
    author_email='komalsswami@gmail.com',
    license='Custom License',  # Update this if using a different license
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Minimum Python version
)
