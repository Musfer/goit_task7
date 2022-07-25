from setuptools import setup, find_namespace_packages

setup(
      name='clean_folder',
      version='1.0.3',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={
            'console_scripts': ['clean-folder=clean_folder.clean:main'],
      },
      # #url='http://github.com/dummy_user/useful',
      # author='Musfer',
      # #author_email='flyingcircus@example.com',
      # license='MIT',
      # packages=find_packages,
)