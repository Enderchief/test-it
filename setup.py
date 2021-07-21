import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

gh = 'https://github.com/endercheif/testit'

setuptools.setup(
    name='TestIt',
    version='0.0.1',
    author='Reet Singh',
    author_email='reet22singh+test.it@gmail.com',
    description='A simple test framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=gh,
    project_urls={
        'Bug Tracker': f'{gh}/issues',
        'Documentation': f'{gh}'
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir={'': 'lib'},
    packages=setuptools.find_packages(where='lib'),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'testit = testit.__main__:main'
        ]
    },
)