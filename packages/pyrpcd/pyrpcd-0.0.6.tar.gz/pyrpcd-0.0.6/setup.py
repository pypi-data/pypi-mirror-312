from setuptools import setup, find_packages

setup(
	name='pyrpcd',
	version='0.0.6',
	author='aiyojun',
	author_email='aiyojun@gmail.com',
	description='Run a RPC server by the most convenient way',
	long_description=open('README.rst').read(),
	url='https://github.com/aiyojun/pysolv',
	packages=find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3',
	],
	python_requires='>=3.6',
	install_requires=[
		'tornado>=6.4.1',
		'voxe==0.0.3'
	],
)