from setuptools import setup, find_packages

setup(
    name='RamanFWHM',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'numpy',
        'matplotlib',
        'pandas',
        'ramanspy',
        'lmfit',
    ],
    entry_points={
        'console_scripts': [
            'your-app-name = your_package_name.setup:main',
        ],
    },
)

