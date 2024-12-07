from setuptools import setup, find_packages


setup(
    name='totemlib',
    version='0.1.0.31',
    packages=find_packages(),
    install_requires=[
        # lista de dependencias
        'jproperties==2.1.2',
        'setuptools==75.6.0',
        'six==1.16.0',
        'wheel==0.45.1'
    ],
    author='Totem Bear',
    author_email='info@totembear.com',
    description='Base library for general uses',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
