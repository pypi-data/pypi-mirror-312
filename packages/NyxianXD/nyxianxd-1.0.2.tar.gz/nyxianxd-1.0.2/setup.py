from setuptools import setup, find_packages

setup(
    name="NyxianXD",
    version="1.0.2",
    description="Library Python untuk uploader Nyxian Network.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Katsu",
    author_email="support@nyxiannetwork.web.id",
    url="https://github.com/nyxiancode",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
