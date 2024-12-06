from setuptools import setup, find_packages

setup(
    name="carvalue_calculator",
    version="0.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Your Name",
    author_email="your.email@example.com",
    description="Simple calculator for car valuations",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)