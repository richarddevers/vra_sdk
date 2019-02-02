from setuptools import setup
from setuptools.command.install import install


setup(name='vra_sdk',
      version="0.0.1",
      description='vra_sdk',
      url='',
      author='',
      author_email='',
      license='MIT',
      include_package_data=True,
      packages=['vra_sdk', 'vra_sdk.models'],
      install_requires=[
          "pbr", 'requests', 'dateutils', 'urllib3'
      ],
      zip_safe=False
      )
