from setuptools import setup, find_namespace_packages
# Install quoi, feur and coubeh, who are all in src/
setup(
    name="quoi",
    url="https://github.com", 
    author="Timothé Boulet",
    author_email="timothe.boulet0@gmail.com",
    
    packages=find_namespace_packages(),

    version="1.0",
    license="MIT",
    description="bruh",
)