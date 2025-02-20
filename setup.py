from setuptools import setup, find_packages

setup(
    name="srscloud-integration",
    version="0.2.1",
    author="Automate Brasil",
    author_email="cx@automate.com",
    description="Integração com SRSCloud para automação de processos",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Automate-Brasil/srscloud-integration",
    packages=find_packages(),
    install_requires=[
        "requests",
        "urllib3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
)
