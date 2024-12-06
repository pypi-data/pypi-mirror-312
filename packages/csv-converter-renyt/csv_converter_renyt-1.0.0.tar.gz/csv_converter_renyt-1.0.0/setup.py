from setuptools import setup, find_packages

setup(
    name='CSVFile-Convert-RYT',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            "csv_convert=cls:main"
        ]
    },
    author='REB YuanTong',
    author_email='renyt1621@mails.jlu.edu.cn',
)