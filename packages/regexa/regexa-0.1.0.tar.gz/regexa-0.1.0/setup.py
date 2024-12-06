from setuptools import setup, find_packages

setup(
    name='regexa',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Brian Adi',
    author_email='uix.brianadi@gmail.com',
    description='A modern, full-featured regex library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bri-anadi/regexa',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
    ],
    python_requires='>=3.6',
    keywords='regex, regular expressions, text processing, validation',
)
