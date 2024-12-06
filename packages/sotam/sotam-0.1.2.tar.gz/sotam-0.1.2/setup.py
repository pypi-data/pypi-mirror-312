from setuptools import setup, find_packages

setup(
    name='sotam',
    version='0.1.2', 
    author='Anandaram Ganapathi',
    author_email='anandaram.ganapathi@gmail.com',
    description="SOTAM-VLSTM: An advanced LSTM framework for time-series prediction and sequential data tasks. It automates preprocessing, optimizes training, supports multi-GPU setups, and provides interactive visualizations. Perfect for applications in finance, IoT, healthcare, and beyond.",
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    url='https://github.com/anand-lab-172/STOAM', 
    license='MIT', 
    packages=find_packages(),
    python_requires='>=3.6', 
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0',
        'tensorflow>=2.6.0',
        'keras>=2.6.0',
        'plotly>=5.0.0',
    ],  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)