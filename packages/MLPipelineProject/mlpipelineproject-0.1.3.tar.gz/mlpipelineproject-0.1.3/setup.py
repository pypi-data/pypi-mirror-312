from setuptools import setup, find_packages

# Read long description from the README file safely
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="MLPipelineProject",  # Your package name
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'xgboost'
    ],
    entry_points={
        'console_scripts': [
            "ml-pipeline=ml_pipeline.app:main",  # Entry point for running Streamlit app
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jhansi Siriprolu',
    author_email='siriprolu2018@gmail.com',
    description='A package for EDA with Streamlit dashboard',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
