from setuptools import setup, find_packages
setup(
      name='clean_folder',
      version='1.0.2',
      entry_points={
            'console_scripts': ['clean-folder=clean_folder.main:main'],
      }
      # description='File sorter',
      # #url='http://github.com/dummy_user/useful',
      # author='Musfer',
      # #author_email='flyingcircus@example.com',
      # license='MIT',
      # packages=find_packages,
)