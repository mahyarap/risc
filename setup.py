from setuptools import setup, find_packages


setup(
    name='risc',
    version='1.0.0',
    description='RISC',
    author='Mahyar Abbaspour',
    author_email='mahyar.abaspour@gmail.com',
    url='https://github.com/mahyarap/risc',
    platforms=['Any'],
    python_requires='>=3.9.0',
    scripts=['bin/risc'],
    install_requires=[],
    extras_require={
        'dev': [
            'pytest==7.1.2',
            'flake8==4.0.1',
        ]
    },
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
)
