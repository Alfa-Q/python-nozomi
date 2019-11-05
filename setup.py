"""Setup package for py-pi"""

from distutils.core import setup


setup(
  name='python-nozomi',
  packages=['nozomi'],
  version='1.0',
  license='MIT',
  description='Nozomi API for retrieving images, videos, gifs.',
  author='Alfa_Q',
  author_email='alfakyuu@gmail.com',
  url='https://github.com/Alfa-Q/python-nozomi',
  download_url='https://github.com/Alfa-Q/python-nozomi/archive/1.0.tar.gz',
  keywords=['nozomi', 'nozomi.la', 'api', 'video', 'image', 'anime'],
  install_requires=[
          'requests',
          'dacite',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
