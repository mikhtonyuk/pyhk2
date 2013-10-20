from setuptools import setup, find_packages

setup(name='pyhk2',
      version='0.1',
      description='Hundred-Kilobyte Kernel library for dependency injection and service discovery',
      url='https://github.com/mikhtonyuk/pyhk2',
      author='Sergii Mikhtoniuk',
      author_email='mikhtonyuk@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['test*']),
      zip_safe=False,
      test_suite='test')