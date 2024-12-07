from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='mulenpay_api',
  version='1.0.12',
  author='WALLEXFINTECH',
  author_email='platem9@gmail.com',
  description='Прием платежей и выплаты через Mulen Pay',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['pydantic', 'httpx'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='payment Mulen Pay wallex',
  project_urls={
    'Documentation': 'https://mulenpay.ru/docs/api'
  },
  python_requires='>=3.8'
)