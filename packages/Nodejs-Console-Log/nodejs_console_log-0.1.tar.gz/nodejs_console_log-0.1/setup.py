from setuptools import setup, find_packages

setup(
    name='Nodejs-Console-Log',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    description='A Python package that makes the command form Node.js/JavaScript console.log()',
    long_description=open('README.md').read() if open('README.md').closed == False else '',
    long_description_content_type='text/markdown',
    author='BARTEKK23',
    author_email='minbartek41@gmail.com',
    url='https://github.com/Bartosz8291/Nodejs-Console-Log',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
