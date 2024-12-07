from setuptools import setup, find_packages

setup(
    name="my_code_display",  # Unique name for your package
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "code-display=my_code_display.main:main",
        ],
    },
    author="Mmm",
    description="A simple package that displays code when asked.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_code_display",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
