from setuptools import setup, find_packages

setup(
    name="legacy_font_converter",  
    version="0.1.0",  # Increment with each release
    description="A tool for converting legacy fonts",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Abdur Rahim Sheikh (Abir)",
    author_email="abi.rahim.sheikh@example.com",
    url="https://github.com/Abdur-Rahim-sheikh/legacy-font-converter",
    packages=find_packages(),
    include_package_data=True,  # To include non-Python files like JSON
    install_requires=[],  # Add any dependencies here (e.g., 'numpy', 'requests')
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
