from setuptools import setup, find_packages

setup(
    name="crowdstrike-foundry",
    version="20.3.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="CrowdStrike Foundry Integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crowdstrike-foundry",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)