from distutils.core import setup
from setuptools import find_packages


with open("README.rst", "r") as f:
    long_description = f.read()


# 每次更新记得改版本
setup(name='fwhassess',
    version='1.0.2',
    description='A standard code base for model performance evaluation.',
    long_description=long_description,
    author='lotuslaw',
    author_email='Lotuslaw.Ni@franklinwh.com',
    url='',
    install_requires=["scikit-learn", "pandas", "numpy", "matplotlib"],
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ])