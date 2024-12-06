from setuptools import setup, find_packages

setup(
    name="auth0-open-source-template",
    version="20.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A template package for Auth0 open source projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/auth0-open-source-template",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)