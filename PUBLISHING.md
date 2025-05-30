# Publishing EdgeX Python SDK to PyPI

This guide explains how to publish the EdgeX Python SDK to PyPI without using personal accounts.

## Prerequisites

### 1. Create Organization PyPI Account

1. Go to [PyPI Registration](https://pypi.org/account/register/)
2. Create an account using the organization email (e.g., `info@edgex.exchange`)
3. Verify the email address
4. Enable 2FA for security

### 2. Create API Tokens

For security, use API tokens instead of passwords:

1. Log into the organization PyPI account
2. Go to Account Settings → API tokens
3. Create a new API token:
   - **Name**: `edgex-python-sdk-upload`
   - **Scope**: Limit to specific project (after first upload)
4. Copy and securely store the token (starts with `pypi-`)

### 3. Set up GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token
   - `TEST_PYPI_API_TOKEN`: Your Test PyPI API token (optional, for testing)

## Publishing Methods

### Method 1: Automated Publishing via GitHub Actions (Recommended)

This method automatically publishes when you create a GitHub release:

1. **Create a release**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
   
2. **Create GitHub release**:
   - Go to GitHub → Releases → Create a new release
   - Choose the tag you just created
   - Add release notes
   - Publish the release

3. **GitHub Actions will automatically**:
   - Build the package
   - Run quality checks
   - Upload to PyPI

### Method 2: Manual Publishing

If you prefer manual control:

1. **Install build tools**:
   ```bash
   pip install build twine
   ```

2. **Build the package**:
   ```bash
   python scripts/build_and_test_package.py
   ```

3. **Upload to Test PyPI first** (recommended):
   ```bash
   twine upload --repository testpypi dist/*
   ```
   
4. **Test installation from Test PyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ edgex-python-sdk
   ```

5. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

## Testing Before Publishing

### Local Testing

1. **Build and test locally**:
   ```bash
   python scripts/build_and_test_package.py
   ```

2. **Install locally**:
   ```bash
   pip install dist/edgex_python_sdk-*.whl
   ```

3. **Test basic functionality**:
   ```python
   import edgex_sdk
   print(edgex_sdk.__version__)
   ```

### Test PyPI

Always test on Test PyPI before publishing to the main PyPI:

1. **Upload to Test PyPI**:
   ```bash
   twine upload --repository testpypi dist/*
   ```

2. **Install from Test PyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ edgex-python-sdk
   ```

## Version Management

Update version numbers in these files before publishing:

1. `setup.py` - line with `version="x.x.x"`
2. `pyproject.toml` - line with `version = "x.x.x"`
3. `edgex_sdk/__init__.py` - add `__version__ = "x.x.x"`

## Security Best Practices

1. **Use API tokens**, not passwords
2. **Enable 2FA** on PyPI account
3. **Limit token scope** to specific projects
4. **Store tokens securely** in GitHub Secrets
5. **Rotate tokens regularly**
6. **Never commit tokens** to version control

## Troubleshooting

### Common Issues

1. **Package name already exists**:
   - Choose a different name in `setup.py` and `pyproject.toml`

2. **Version already exists**:
   - Increment version number
   - You cannot overwrite existing versions on PyPI

3. **Authentication failed**:
   - Check API token is correct
   - Ensure token has proper permissions

4. **Build fails**:
   - Run `python scripts/build_and_test_package.py` locally
   - Check for missing dependencies or syntax errors

### Getting Help

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- GitHub Actions: https://docs.github.com/en/actions

## Post-Publishing

After successful publishing:

1. **Test installation**:
   ```bash
   pip install edgex-python-sdk
   ```

2. **Update documentation** if needed

3. **Announce the release** to users

4. **Monitor for issues** and user feedback
