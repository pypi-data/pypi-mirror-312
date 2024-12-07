from setuptools import setup, find_packages

setup(
    name="astrogator",
    version="1.0.0",
    author="Koustubh PK",
    author_email="koustubhpk@example.com",
    description="Astrogator: Your daily guide to the stars, offering personalized horoscopes with ease.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/horoscope_package",
    packages=find_packages(),
    install_requires=[
    "requests",
    "beautifulsoup4"
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
