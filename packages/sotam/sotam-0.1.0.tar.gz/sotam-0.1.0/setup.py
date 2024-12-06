from setuptools import setup, find_packages

setup(
    name='sotam',
    version='0.1.0', 
    author='Anandaram Ganapathi',
    author_email='anandaram.ganapathi@gmail.com',
    description='A finest arch of LSTM',
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    url='https://github.com/anand-lab-172/STOAM', 
    license='MIT', 
    packages=find_packages(),
    python_requires='>=3.6', 
    install_requires=[],  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)