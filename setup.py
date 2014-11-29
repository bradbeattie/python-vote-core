import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
LICENSE = open(os.path.join(here, 'LICENSE.txt')).read()

requires = [
    'python-graph-core >= 1.8.0',
    'six >= 1.8.0',
]

setup(name='python-vote-core',
      version='20120423.0',
      description="An implementation of various election methods, most notably the Schulze Method and Schulze STV.",
      long_description=README + '\n\n' + CHANGES + '\n\n' + LICENSE,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Topic :: Scientific/Engineering :: Mathematics",
      ],
      author='Brad Beattie',
      author_email='bradbeattie@gmail com',
      url='https://github.com/bradbeattie/python-vote-core',
      license='GPLv3',
      keywords='library election',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="test_functionality",
      )
