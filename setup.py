from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='inoreader',
      version='0.1',
      description='',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      keywords='utilities dryx',
      # url='https://github.com/thespacedoctor/inoreader',
      author='thespacedoctor',
      author_email='davidrobertyoung@gmail.com',
      license='MIT',
      packages=['inoreader'],
      include_package_data=True,
      install_requires=[
          'pyyaml',
          'requests',
          'ndg-httpsclient'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['inoreader=inoreader.cl_utils:main'],
      },
      zip_safe=False)
