from setuptools import find_packages, setup

PKG_NAME = 'prlps-translit'
VERSION = '0.0.1'

setup(
    name=PKG_NAME,
    version=VERSION,
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/prolapser/prlps_translit',
    license='LICENSE.txt',
    description='веб поиск',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
