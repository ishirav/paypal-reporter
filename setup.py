from distutils.core import setup

PACKAGE = "paypal_reporter"
NAME = "paypal_reporter"
DESCRIPTION = "A library to generate reports about activity in a PayPal account"
AUTHOR = "Itai Shirav"
AUTHOR_EMAIL = "itai@platonix.com"
URL = "https://github.com/ishirav/paypal-reporter"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=['paypal_reporter'],
    install_requires =['requests>=1.0', 'tabulate'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)