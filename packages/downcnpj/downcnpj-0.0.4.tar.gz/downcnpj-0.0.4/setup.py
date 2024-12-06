from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='downcnpj',
    version='0.0.4',
    license='MIT License',
    author='Anthony Matheus',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='anthonymatheusds@gmail.com.br',
    keywords='download cadastro nacional pessoa juridica cnpj',
    description=u'download cadastro nacional cnpj',
    packages=['downcnpj'],
    install_requires=['requests', 'bs4'],)