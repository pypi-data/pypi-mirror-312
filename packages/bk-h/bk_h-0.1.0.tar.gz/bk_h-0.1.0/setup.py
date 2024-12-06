from setuptools import setup, find_packages

setup(
    name="bk_h",  # The name of your package
    version="0.1.0",  # Initial version
    packages=find_packages(),
    description="A short description of my package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # List dependencies here, e.g., 'numpy', 'requests'
    ],
)
