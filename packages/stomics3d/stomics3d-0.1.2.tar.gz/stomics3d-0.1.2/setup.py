
#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.2'

setup(name='stomics3d',
      version=VERSION,
      description="A web server for visualization of spatial-temporal single cell transcriptomics data",
      long_description='A test release',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python single cell transcriptomics 3D visualization spatial temporal',
      author='wuc',
      author_email='1078497976@qq.com',
      url='https://github.com/twocucao/doumu.fm',
      license='GNU GPLv3',
      packages=find_packages(),
      install_requires=[
        'dash==2.16.1',
        'dash-bootstrap-components',
        'dash-extensions',
        'dash-iconify',
        'dash-mantine-components==0.12.1',
        'feffery-antd-components',
        'feffery-utils-components',
        'plotly',
        'scanpy==1.9.8',
        'squidpy',
        'pandas==2.2.1',
        'numpy==1.23.4',
        'numba==0.59.0',
        'typing',
        'typing_extensions',
        'diskcache',
        'fastapi',
        'uvicorn'
      ],
      zip_safe=False,
      entry_points={
        'console_scripts':[
            'stomics3d = app:main'
        ]
      },
)
 