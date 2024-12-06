from setuptools import setup, find_packages

setup(
    name="cgpa_calculator",
    version="2.2.0",
    description="A Python-based CGPA Calculator to manage courses and calculate weighted CGPA.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="S.M.Abrar Mustakim Taki",
    author_email="abrar.mustakim@bjitacademy.com",  # Replace with your email
    url="https://github.com/Mustakim-Taki/cgpa_calculator",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
