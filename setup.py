from setuptools import setup

setup(
    name='mmdok-cli',
    version='1.4',    
    description='Cli client for TinyDS',
    url='https://github.com/emagnca/mmcli',
    author='emagnca',
    author_email='ehsmaga@yahoo.se',
    license='BSD 2-clause',
    packages=['mmcli'],
    install_requires=['cmd2==1.5.0',
                      'requests==2.25.0',
                      'urllib3==1.26.2'],
    entry_points={
        'console_scripts': [
            'mmcli=mmcli.mmcli:main',
            'mmadmin=mmcli.mmadmin:main',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',       
        'Programming Language :: Python :: 3 :: Only'
    ],
)
