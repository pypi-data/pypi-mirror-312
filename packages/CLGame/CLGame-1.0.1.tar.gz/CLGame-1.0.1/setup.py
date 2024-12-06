from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='CLGame',
  version='1.0.1',
  author='Korsy',
  author_email='pgeorg@gmail.com',
  description='Module that helps to create games in terminal',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/K0RSY/CLGame',
  packages=find_packages(),
  install_requires=['playsound>=1.3.0', 'pynput>=1.7.7'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent'
  ],
  keywords='game engine cli tui terminal console',
  project_urls={
    'Wiki': 'https://github.com/K0RSY/CLGame/wiki'
  },
  python_requires='>=3.10'
)
