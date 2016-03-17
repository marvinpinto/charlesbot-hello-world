from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: add any additional package requirements here
    'charlesbot',
]

test_requirements = [
    # TODO: add any additional package test requirements here
    'asynctest',
    'coverage',
    'flake8',
]

setup(
    name='charlesbot-hello-world',
    version='0.0.1',
    description="Hello World example for Charlesbot",
    long_description=readme,
    author="Marvin Pinto",
    author_email='marvin@pinto.im',
    url='https://github.com/marvinpinto/charlesbot-hello-world',
    packages=[
        'charlesbot_hello_world',
    ],
    package_dir={'charlesbot_hello_world':
                 'charlesbot_hello_world'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='slack robot chatops charlesbot charlesbot-hello-world',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)
