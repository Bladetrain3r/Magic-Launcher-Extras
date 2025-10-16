from setuptools import setup, find_packages

setup(
    name="cpu-load-mapper",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CPU Load Mapping system utilizing rhythmic analysis and topological mapping.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cpu-load-mapper",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "psutil",
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)