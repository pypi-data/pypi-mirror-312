from setuptools import setup, find_packages

setup(
    name="mlops_observation",
    version="0.1.1",
    packages=find_packages(where='source'),
    package_dir={"": "source"},
    include_package_data=True,
    install_requires=[
        'evidently==0.4.39',
        'pandas==2.2.3',
        'numpy==2.0.2'
    ],
    long_description='README.md',  # Add README content
    long_description_content_type="text/markdown",  # Specify Markdown format
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust license type if needed
        "Operating System :: OS Independent",
    ],
)