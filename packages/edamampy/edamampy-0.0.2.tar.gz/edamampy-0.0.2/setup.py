from setuptools import setup, find_packages
setup(
    name='edamampy',
    version='0.0.2',
    packages=find_packages(include=['edamampy, edamampy.*']),
    install_requires=[
        'annotated-types>=0.7.0',
        'certifi>=2024.8.30',
        'charset-normalizer>=3.4.0',
        'idna>=3.10',
        'pydantic>=2.9.2',
        'pydantic_core>=2.23.4',
        'python-dateutil>=2.9.0.post0',
        'requests>=2.32.3',
        'six>=1.16.0',
        'typing_extensions>=4.12.2',
        'urllib3>=2.2.3',
    ],
    entry_points={
        'console_scripts': ['cli=edamam.__main__:main']
    }
)
