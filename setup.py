from setuptools import setup, find_packages

setup(
    name='tts-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'azure-cognitiveservices-speech',
        'PyPDF2',
        'python-docx',
    ],
    entry_points={
        'console_scripts': [
            'tts=tts_cli.main:main',
        ],
    },
)
