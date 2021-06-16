from setuptools import setup

setup(
    name='movies_analysis',
    version='0.1',
    description='movies_analysis',
    url='https://github.com/enavu/sdr_avail.git',
    author='Ena Vu',
    author_email='ena@enavu.io',
    license='MIT',
    packages=['movies_analysis'],
    install_requires=[
        'pandas',
        'pandasql'
    ],
    python_requires='>=3.6',
    zip_safe=False)