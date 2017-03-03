from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='thedoorman',
    version='0.1',
    description='Remote Doorman',
    long_description=readme,
    author='Dave Ehrenberger',
    author_email='dave.ehrenberger@focusedsupport.com',
    url='https://github.com/FocusedSupport/thedoorman',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'slackbot',
        ]
)
