from setuptools import setup, find_packages

setup(
    name='RamanFWHMAnalyzer',
    version='1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # 添加其他依赖项
    ],
    entry_points={
        'console_scripts': [
            'run_raman_fwhm = main:main',
        ],
    },
)