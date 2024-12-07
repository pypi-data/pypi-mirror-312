from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="fnyzer",
    version="1.3.10",
    description="Flexible Nets analYZER",
    url='https://bitbucket.org/Julvez/fnyzer',
    long_description=readme(),
    packages=find_packages(),
    entry_points={
        'console_scripts': ['fnyzer=fnyzer.fnyzer:main']
    },
    install_requires=[
       'pyomo>=6.8.2',
       'numpy>=2.1.0', # pyomo 6.7 does not seem to be compatible with numpy 2.0
       'xlwt>=1.3.0',
       'matplotlib>=3.0.0',
       'statsmodels>=0.10.1'
    ],
    author="Jorge Julvez",
    author_email="fnyzer@unizar.es",
    license="GNU GENERAL PUBLIC LICENSE",
    keywords="flexible nets analyzer",
)
