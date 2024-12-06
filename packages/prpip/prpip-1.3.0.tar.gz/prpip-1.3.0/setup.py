from setuptools import setup, find_packages

setup(
    name="prpip",
    use_scm_version=True,
    setup_requires=["setuptools-scm"],
    author="Mohammad Ahsan Khodami",
    description="A package for reconstructing pupil size and handling eye-tracker blinks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AhsanKhodami/prpip",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "pandas",
    ],
)
