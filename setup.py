from setuptools import setup, find_packages

setup(
    name="vxtwitter",
    version="0.1.0a",
    url='http://github.com/praekelt/vumi-twitter',
    license='BSD',
    description="A Twitter transport for Vumi.",
    long_description=open('README.md', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekeltfoundation.org',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'vumi',
        # We need a dev versions of the packages above, so they have to be
        # installed before us. They're listed first so that we fail fast
        # instead of working through all the other requirements before
        # discovering that they aren't available should that be the case.
        'Twisted>=13.1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],
)
