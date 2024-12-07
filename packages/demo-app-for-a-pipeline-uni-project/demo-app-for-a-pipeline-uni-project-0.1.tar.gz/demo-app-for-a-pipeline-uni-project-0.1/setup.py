from setuptools import setup, find_packages


setup(
    name='demo-app-for-a-pipeline-uni-project',  # Replace with your project name
    version='0.1',
    packages=find_packages(),  # Automatically find and include packages in your project
    install_requires=[          # List the dependencies here
        'flask'                 # Example dependency          
    ],
    classifiers=[  # Additional metadata (optional)
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Specify minimum Python version
)

