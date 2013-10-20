from setuptools import setup, find_packages

setup(name='pyhk2',
      version='0.1',
      description='Hundred-Kilobyte Kernel library for dependency injection and service discovery',
      url='https://github.com/mikhtonyuk/pyhk2',
      author='Sergii Mikhtoniuk',
      author_email='mikhtonyuk@gmail.com',
      license='MIT',
      packages=['hk2', 'hk2.annotations', 'hk2.extensions', 'hk2.injection', 'hk2.kernel', 'hk2.types', 'hk2.utils', 'hk2.extensions.impl', 'hk2.kernel.plugin_loaders', 'hk2.extensions.impl.declarative'],
      zip_safe=False,
      test_suite='test')