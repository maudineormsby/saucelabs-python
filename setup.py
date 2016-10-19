from setuptools import setup


setup(
    name='saucelabs-python',
    version='0.3',
    description='REST Client for Saucelabs API',
    url='https://github.com/maudineormsby/saucelabs-python',
    author='Jason Carr',
    author_email='jason.s.carr@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords=[
        'sauce',
        'saucelabs',
        'rest',
        'development',
        'python client',
        'automation',
        'selenium',
        'webdriver',
    ],
    packages=['sauce'],
    install_requires=['requests >= 2.2.1'],
)
