from setuptools import setup

setup(
    name='Satellite',
    version='0.0.5',
    long_description=__doc__,

    author='Ellen Bowman',
	author_email='ebowman@fool.com',
	url='https://bitbucket.org/ebowman/hackathon-for-real',

    packages=['content_satellite'],
    include_package_data=False,
    zip_safe=False,
    install_requires=['Django==1.7.3',]
)