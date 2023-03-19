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
            'pytest',
            'pylint',
            'black',
        ],
    },
)
