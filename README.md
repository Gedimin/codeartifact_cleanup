# codeartifact_cleanup
Script to cleaning up CodeArtifact from old packages

# Dependencies:
Modules `boto3` and `python-dotenv` will be instaled.
```bash
poetry install
```

# Usage
You need to have aws cli installed and configured.
Create .env file with variables mentioned in script:
```bash
cat << EOF > .env
domain_name=test
repository_name=test_repo
format_artifact=maven
domain_owner=123456789123
artifact_status_to_delete=Unlisted
EOF
```

Just run:
```bash
poetry run python codeartifact_cleanup.py
```
