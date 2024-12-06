from setuptools import setup, find_packages

setup(
    name="agentmesh",  # Package name
    version="0.1.0",
    author="Aboyai Inc",
    author_email="abhilashk.cse@gmai.com",
    description="Placeholder for reserving the agentmesh package name.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://agentmesh.org",  # Replace with your project URL
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",  # Use Apache License
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
)
