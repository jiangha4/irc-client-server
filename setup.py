import setuptools

setuptools.setup(
    version="0.1.0",
    name="irc-server",
    package_dir={"": "src"},
    test_suite="tests",
    python_requires=">=3.7",
    description="IRC Server",
    url="https://github.com/jiangha4/irc-client-server",
    author="davidjiang.haohan@gmail.com",
    extras_require={
        "test": [
            'pytest==7.1.3',
            'pytest-html==3.1.1',
            'pytest-cov',
            'pylint',
            'jinja2',
            'black',
        ],
    },
)
