from Cython.Build import cythonize
from setuptools import setup, find_packages

setup(
    name="checksum_dict",
    description="checksum_dict's objects handle the simple but repetitive task of checksumming addresses before setting/getting dictionary values.",
    author="BobTheBuidler",
    author_email="bobthebuidlerdefi@gmail.com",
    url="https://github.com/BobTheBuidler/checksum_dict",
    packages=find_packages(),
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
    },
    setup_requires=["setuptools_scm", "cython"],
    install_requires=[
        "eth_typing",
        "eth_utils",
    ],
    package_data={
        "checksum_dict": ["py.typed"],
    },
    include_package_data=True,
    ext_modules=cythonize(
        "checksum_dict/**/*.pyx",
        compiler_directives={
            "language_level": 3,
            "embedsignature": True,
            "linetrace": True,
        },
    ),
    zip_safe=False,
)
