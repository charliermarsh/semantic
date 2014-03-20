from distutils.core import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(name='intent',
      version='1.0.1',
      description='Common Natural Language Processing Tasks for Python',
      author='Charles Marsh',
      author_email='crmarsh@princeton.edu',
      url='https://github.com/crm416/intent',
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
      long_description=open('README.txt').read(),
      install_requires=reqs,
      packages=['intent', 'intent.test']
      )
