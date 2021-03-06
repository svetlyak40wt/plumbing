from distutils.core import setup

setup(
        name             = 'plumbing',
        version          = '2.0.1',
        description      = 'Helps with plumbing-type programing in python',
        long_description = open('README.md').read(),
        license          = 'MIT',
        url              = 'http://github.com/xapple/plumbing/',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        classifiers      = ['Topic :: Scientific/Engineering :: Bio-Informatics'],
        packages         = ['plumbing'],
        install_requires = ['sh', 'biopython'],
    )
