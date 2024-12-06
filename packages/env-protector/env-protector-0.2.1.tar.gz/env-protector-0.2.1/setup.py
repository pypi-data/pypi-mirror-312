from setuptools import setup, find_packages

setup(
    name="env-protector",
    version="0.2.1",
    description="Package for managing Git hooks to encrypt and decrypt .env files.",
    long_description="Package for secure .env file management in Git.",
    long_description_content_type="text/markdown",
    author="Lech Hubicki",
    author_email="lech.hubicki@gmail.com",
    url="https://github.com/lechplace/env-protector",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "env-protector=env_protector.hooks_manager:main",
        ],
    },
)
