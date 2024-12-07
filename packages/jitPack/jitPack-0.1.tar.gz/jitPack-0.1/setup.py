from setuptools import setup, find_packages

setup(
    name="jitPack",  
    version="0.1",          
    packages=find_packages(),
    author="zouhir dev",     
    description="A Python package to facilitate the interaction with JIT_API",
    install_requires=[
        'fastapi==0.115.2',         
        'uvicorn==0.32.0',         
        'Rx==3.2.0',               
        'requests==2.32.3',        
        'keyring==25.4.1',         
        'jsonschema==4.23.0',
        'pydantic==2.9.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

