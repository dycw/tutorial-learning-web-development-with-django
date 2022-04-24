from re import MULTILINE
from re import findall

from setuptools import find_packages
from setuptools import setup


with open(".bumpversion.cfg") as fh:
    (version,) = findall(
        r"^current_version = (\d+\.\d+\.\d+)$", fh.read(), flags=MULTILINE
    )
with open("README.md") as fh:
    long_description = fh.read()


setup(  # https://bit.ly/3MJfVyH
    name="app",
    version=version,
    description="Learning Web Development with Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Derek Wan",
    author_email="d.wan@icloud.com",
    url="https://github.com/dycw/tutorial-learning-web-development-with-django",  # noqa: E501
    packages=find_packages("src"),
    options={"bdist_wheel": {"universal": "1"}},
    license="MIT",
    license_files=["LICENSE"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "beartype >= 0.10.4, < 0.11",
        "django >= 4.0.4, < 4.1",
        "pillow >= 9.1.0, < 9.2",
        "plotly >= 5.7.0, < 5.8",
        "xlsxwriter >= 3.0.3, < 3.1",
        # django extensions
        "dj-database-url >= 0.5.0, < 0.6",
        "django-configurations >= 2.3.2, < 2.4",
        "django-crispy-forms >= 1.14.0, < 1.15",
        "django-debug-toolbar >= 3.2, < 3.3",
        "djangorestframework >= 3.13.1, < 3.14",
    ],
    entry_points={"console_scripts": []},
    extras_require={
        "dev": [
            # development
            "build >= 0.7.0, < 0.8",
            "bump2version >= 1.0.1, < 1.1",
            "pip-tools >= 6.6.0, < 6.7",
            "pre-commit >= 2.18.1, < 2.19",
            "pyclean >= 2.2.0, < 2.3",
            # formatters
            "black >= 22.3.0, < 22.4",
            "isort >= 5.10.1, < 5.11",
            # linters
            "flake8 >= 4.0.1, < 4.1",
            "flake8-absolute-import >= 1.0.0.1, < 1.0.1",
            "flake8-annotations >= 2.9.0, < 2.10",
            "flake8-bandit >= 3.0.0, < 3.1",
            "flake8-bugbear >= 22.3.23, < 22.4",
            "flake8-comprehensions >= 3.8.0, < 3.9",
            "flake8-debugger >= 4.0.0, < 4.1",
            "flake8-eradicate >= 1.2.0, < 1.3",
            "flake8-no-pep420 >= 2.2.0, < 2.3",
            "flake8-pie >= 0.15.0, < 0.16",
            "flake8-print >= 4.0.0, < 4.1",
            "flake8-simplify >= 0.19.2, < 0.20",
            "flake8-unused-arguments >= 0.0.9, < 0.1",
            # testing
            "pytest >= 7.1.2, < 7.2",
            "pytest-django >= 4.5.2, < 4.6",
            "pytest-instafail >= 0.4.2, < 0.5",
            "pytest-xdist >= 2.5.0, < 2.6",
            # typing
            "django-stubs >= 1.10, < 2",
        ]
    },
    python_requires=">= 3.10.4",
)
