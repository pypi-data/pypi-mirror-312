import os
from setuptools import setup, find_packages

setup(
    name="st-autorefresh",
    version=os.getenv("ST_AUTOREFRESH_VERSION", "0.1.0"),  # Default to 0.1.0 if not set
    description="A Streamlit component for automatically refreshing the page at a user-defined interval.",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.txt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/meet2147/st-autorefresh",  # Update with your GitHub URL
    author="Meet Jethwa",
    author_email="meetjethwa3@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        
    ],
    python_requires=">=3.6",
    keywords="streamlit, autorefresh, real-time, component",
)
