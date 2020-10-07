#### Contributing

When contributing to `hickory`, please open an issue before making a change


#### Development environment and steps

1. Install `pytest` either globally or in a virtualenv: `pip install pytest`
2. Click on the "Fork" button at the top-right of the GitHub page
3. Clone your fork: `git clone git@github.com:yourname/gazpacho.git`
4. Create a new branch to work on the issue/feature you want
5. Hack out your code. 
6. Runs the tests by executing `pytest` from the command line (note, some tests will not work on specific platforms)
7. Submit a new PR with your code, indicating in the PR which issue/feature it relates to

#### Guidelines

- Keep in mind that `hickory` does not want to do everything
- Always write tests for any change introduced
- If the change involves new methods, arguments or otherwise modifies the public API, make sure to adjust the `README.md`
- If the change is beyond cosmetic, add it to the `CHANGELOG.md` file and give yourself credit!
