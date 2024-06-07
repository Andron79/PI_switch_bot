from setuptools import setup, find_packages
import tolik_bot


setup(
    name='tolik-bot',
    version=tolik_bot.__version__,
    description='tolik_bot_package',
    long_description='',
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9.2',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
    ],
    author='Andrew Zhabkin',
    author_email='azhabkin@getmobit.ru',
    url='http://rpi0.kknd.gm.corp:8000/docs',
    license='Getmobit LLC',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'tolik-bot = tolik_bot.main:main'
        ]
    },
    install_requires=[
        'anyio==3.6.1',
        'asgiref==3.5.2',
        'click==8.1.3',
        'fastapi==0.78.0',
        'h11==0.13.0',
        'httptools==0.4.0',
        'idna==3.3',
        'pydantic==1.9.1',
        'python-dotenv==0.20.0',
        'PyYAML==6.0',
        'RPi.GPIO==0.7.1',
        'sniffio==1.2.0',
        'starlette==0.19.1',
        'typing_extensions==4.2.0',
        'uvicorn==0.17.6',
        'uvloop==0.16.0',
        'watchgod==0.8.2',
        'websockets==10.3'
    ],

    extras_require={
        "test": [
            "flake8",
            "coverage==5.5",
            "Mock.GPIO==0.1.8",
            "pytest==5.4.1",
            "pytest-cov==2.12.1",
            "requests==2.28.1"
        ],
        "develop": "bump2version"
    },
)
