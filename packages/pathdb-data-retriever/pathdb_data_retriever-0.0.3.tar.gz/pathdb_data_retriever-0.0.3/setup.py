from setuptools import setup, find_packages

setup(
    name='pathdb-data-retriever',
    version='0.0.3',
    description='A tool for downloading TCIA pathology images using Excel manifests to specify download URLs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Justin Kirby',
    author_email='justin.kirby@nih.gov',
    url='https://github.com/kirbyju/pathDB-Data-Retriever',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'PyQt5',
    ],
    entry_points={
        'console_scripts': [
            'pathDB-Data-Retriever=pathology_downloader.downloader:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
