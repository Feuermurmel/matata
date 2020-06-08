import setuptools

name = 'matata'
dependencies = []
dependencies_dev = []
console_scripts = ['matata = matata:entry_point']

setuptools.setup(
    name=name,
    entry_points=dict(console_scripts=console_scripts),
    install_requires=dependencies,
    extras_require={'dev': dependencies_dev},
    setup_requires=['setuptools>=42', 'wheel', 'setuptools_scm[toml]>=3.4'],
    use_scm_version=True,
    include_package_data=True,
    packages=setuptools.find_packages(exclude=['tests']))
