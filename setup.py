#!/usr/bin/env python
from setuptools import setup, find_packages
import pkg_resources
import sys
import os



try:
    if int(pkg_resources.get_distribution("pip").version.split('.')[0]) < 6:
        print('pip older than 6.0 not supported, please upgrade pip with:\n\n'
              '    pip install -U pip')
        sys.exit(-1)
except pkg_resources.DistributionNotFound:
    pass

if os.environ.get('CONVERT_README'):
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
else:
    long_description = ''

version = sys.version_info[:2]


if version[0] < 3:
    print('smartass requires Python version 3 or later' + 
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)
    
if (3, 0) < version < (3, 5):
    print('smartass requires Python version 3.5 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)

VERSION = '0.02'

install_requires = ['psutil', 'colorama', 'six', 'google-generativeai', 'google-ai-generativelanguage']
extras_require = {':python_version<"3.4"': ['pathlib2'],
                  ':python_version<"3.3"': ['backports.shutil_get_terminal_size'],
                  ':python_version<="2.7"': ['decorator<5', 'pyte<0.8.1'],
                  ':python_version>"2.7"': ['decorator', 'pyte'],
                  ":sys_platform=='win32'": ['win_unicode_console']}

if sys.platform == "win32":
    scripts = ['scripts\\damn.bat', 'scripts\\damn.ps1']
    entry_points = {'console_scripts': [
                  'smartass = smartass.entrypoints.main:main',
                  'smartass_firstuse = smartass.entrypoints.not_configured:main']}
else:
    scripts = []
    entry_points = {'console_scripts': [
                  'smartass = smartass.entrypoints.main:main',
                  'damn = smartass.entrypoints.not_configured:main']}

setup(name='smartass',
      version=VERSION,
      description="Magnificent app which corrects your previous console command",
      long_description=long_description,
      author='geoffyoon',
      author_email='koock1994@gmail.com',
      url='https://github.com/geoffyoon-dev/smartass-python',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'tests.*', 'release']),
      include_package_data=True,
      zip_safe=False,
      python_requires='!=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
      install_requires=install_requires,
      extras_require=extras_require,
      scripts=scripts,
      entry_points=entry_points)
