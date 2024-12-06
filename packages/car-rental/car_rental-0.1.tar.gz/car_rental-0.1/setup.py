from setuptools import setup, find_packages

setup(
    name="car_rental",            # Name of your project (this is how it will be installed on PyPI)
    version="0.1",                # Version of your project (start with 0.1 for the first release)
    packages=find_packages(),     # Automatically find all Python packages (if you have more subfolders, this will help)
    description="A simple car rental management system",  # Short description of your project
    long_description=open('README.md').read(),  # This reads your README.md for the long description
    long_description_content_type="text/markdown",  # PyPI will know it’s a Markdown file
    author="Your Name",           # Your name or company name
    author_email="your.email@example.com",  # Your email address
    url="https://github.com/yourusername/car_rental",  # Your project's homepage (GitHub or personal site)
    classifiers=[                 # These are optional tags that help users find your project
        "Programming Language :: Python :: 3",  # Your project supports Python 3
        "License :: OSI Approved :: MIT License",  # Assuming you’re using MIT license (you can change it)
        "Operating System :: OS Independent",  # It works on all operating systems
    ],
    python_requires='>=3.6',      # Minimum Python version required
)
