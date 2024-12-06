from setuptools import setup, find_packages

setup(
    name='MTBF_G48',
    version='1.0.2',
    description='marionette driver to establish connection.',
    long_description='marionette_driver for QA testing purpose of devices.',
    license='MIT',
    packages=find_packages(),
    author='shayan',
    author_email='syedshayan109@gmail.com',
    install_requires=['mozrunner==8.3.0',
                      'mozversion==2.4.0',
                      'six==1.16.0',
                      'future==0.18.3',
                      'PyAutoGUI==0.9.54',
                      'opencv-python==4.2.0.32',
                      'manifestparser==2.1.0'],
    keywords=['mtbf_g48', 'g48'],
    download_url='https://pypi.org/project/mtbf_g48/'
)

