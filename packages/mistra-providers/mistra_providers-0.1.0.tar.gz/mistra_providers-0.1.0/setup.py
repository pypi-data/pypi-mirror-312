from setuptools import setup

setup(
    name='mistra-providers',
    version='0.1.0',
    packages=['mistra.providers.historical.preprocessing',
              'mistra.providers.historical.raw.filesystem',
              'mistra.providers.historical.raw.truefx'],
    url='',
    license='MIT',
    author='luismasuelli',
    author_email='luisfmasuelli@gmail.com',
    description='MISTRA Providers contains a collection of custom providers for the MISTRA package',
    python_requires='>=3.12',
    install_requires=['mistra>=0.1.0', 'pandas>=2.2.3']
)
