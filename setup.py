from setuptools import setup, find_packages

with open("app/README.md", "r") as f:
    long_description = f.read()
    
setup(
    name='tvnsrtools',
    version='0.1',
    description='Tools to integrate and test remote triggering for the tVNS-R Stimulator. Features a python class to intefrace with the stimulator and a mock server for testing',
    long_description=long_description,
    long_description_content_type="text/markdown",    
    author='Joshua P. Woller',
    author_email='your@email.com',
    license = 'MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tvnsMockServer = tvnsrtools.tvnsMockServer:main',
        ],
    },
    classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
],
    python_requires=">=3.8",
)
