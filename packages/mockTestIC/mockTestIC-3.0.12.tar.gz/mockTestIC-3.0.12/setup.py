from setuptools import setup

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(
    name='mockTestIC',
    version='3.0.12',
    license='MIT License',
    author='Victor Augusto do Carmo',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='Victoraugustodocarmo32@gmail.com',
    keywords=['mockTest', 'dados falsos', 'insert de dados falsos', 'dados ficticios', 'SQL', 'gerador de dados', 'false data', 'fictitious data', 'data', 'dados', 'data generator'],
    description='Este projeto é uma biblioteca Python chamada mockTestIC que utiliza a biblioteca Faker para gerar dados fictícios com base em um mapeamento pré-definido.',

    packages=['mockTestIC'],
    install_requires=[
        'pydantic',
        'faker',
        'typing-extensions',
        'setuptools',
    ],
)
