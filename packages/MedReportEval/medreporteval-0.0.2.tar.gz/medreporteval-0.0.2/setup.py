from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='MedReportEval',
    version='0.0.2',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],


    install_requires=requirements,
    python_requires='>=3.6',
    # author='Your Name',
    # author_email='youremail@example.com',
    description='A brief description of your package',
    license='MIT',
)