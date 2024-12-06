from setuptools import setup, find_packages

with open('./package_description.rst', 'rt', encoding='utf8') as readme, \
     open('./requirements.txt', 'rt', encoding='utf8') as reqs, \
     open('./LICENSE', 'rt', encoding='utf-8') as lic:
    setup(
        name='asn_viewer',
        maintainer='Sergey Yakimov',
        maintainer_email='sergwy@gmail.com',
        version='0.0.4',
        url='https://gitlab.com/sergwy/asn-viewer',
        description='ASN decoder and viewer',
        long_description_content_type='text/x-rst',
        long_description=readme.read(),
        packages=find_packages(),
        license=lic.read(),
        install_requires=[r for r in reqs],
        entry_points={
            'console_scripts': [
                'asn-viewer = asn_viewer.runapp:main'
            ]
        }
    )
