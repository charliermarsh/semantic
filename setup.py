from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

requires = ['quantities', 'numpy']


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import test
        errno = test.run()
        sys.exit(errno)


setup(name='semantic',
      version='1.0.2',
      description='Common Natural Language Processing Tasks for Python',
      author='Charles Marsh',
      author_email='crmarsh@princeton.edu',
      url='https://github.com/crm416/semantic',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          'Topic :: Text Processing :: Linguistic'
      ],
      install_requires=requires,
      tests_require=requires,
      cmdclass={'test': PyTest},
      long_description=open('README.txt').read(),
      packages=['semantic', 'semantic.test']
      )
