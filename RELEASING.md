# Publishing

Releases are published to PyPI by GitHub Actions. The workflow builds and checks the wheel and source distribution first, then publishes those exact files with PyPI Trusted Publishing. No PyPI password or API token is stored in GitHub.

## One-time setup

1. Create a `pypi` environment in the GitHub repository and add required reviewers to protect it.
2. Add a Trusted Publisher for `api2ch` in PyPI with these values:
   - Owner: `uburuntu`
   - Repository: `api2ch`
   - Workflow: `pythonpublish.yml`
   - Environment: `pypi`

## Release

1. Set `api2ch.__version__` to the release version and merge the change.
2. Run the manual live API workflow and confirm that the current contract checks pass.
3. Create a GitHub release whose tag is `v` followed by the same version, for example `v2.0.0`.
4. Publish the GitHub release.
5. Review the completed build job and approve the `pypi` environment deployment.

The workflow stops before publishing if the tag and package versions do not match, or if either distribution fails its metadata or installation checks.
