# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
from pbox import version

setup(
	name='pandora-bio',
	version=version.__version__,
	description='pandora, a collection of handy functions.',
	url='https://github.com/lijier6/pandora-bio',
	author=version.__author__,
	author_email=version.__email__,

	classifiers=[
				'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
				'Programming Language :: Python :: 3 :: Only',
				'Operating System :: Unix',
	],
	keywords='biology bioinformatics',
	scripts=[version.__scripts__],
	# packages = find_packages(),
	packages=[version.__package__],
	include_package_data=True,
	python_requires='>=3.6',
	install_requires=['ubox>=0.1.0', 'pandas', 'numpy', 'argparse'],
)
