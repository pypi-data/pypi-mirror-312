from setuptools import setup, find_packages

setup(
    name='dialogflow-handler',
    version='0.1.0',
    description='Another Dialogflow API wrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vince Swu',
    author_email='vinceswu88@gmail.com',
    url='https://github.com/ecnivs/dialogflow-handler',
    packages=find_packages(),
    install_requires=[
        'google-cloud-dialogflow',
        'google-api-core'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

