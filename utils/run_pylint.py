from pylint.lint import Run

if __name__ == "__main__":
    Run(["--errors-only", "src", "tests", "client"])