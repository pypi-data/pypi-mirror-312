from setuptools import setup, find_packages

setup(
    name='LocalFinder',
    version='0.1.9',  # Update the version number appropriately
    author='Pengfei Yin',
    author_email='12133074@mail.sustech.edu.cn',
    description='A tool for finding significantly different genomic regions of two tracks using local features.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/astudentfromsustech/LocalFinder',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
        'plotly',
        'pyGenomeTracks',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'localfinder=LocalFinder.__main__:main',
        ],
    },
)
