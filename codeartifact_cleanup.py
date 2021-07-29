import os
import boto3
from dotenv import load_dotenv


load_dotenv()

domain_name = os.environ['domain_name']
repository_name = os.environ['repository_name']
format_artifact = os.environ['format_artifact']
domain_owner = os.environ['domain_owner']
artifact_status_to_delete = os.environ['artifact_status_to_delete']

# By default boto3 uses default profile of aws cli credentials
client = boto3.client('codeartifact')

# #  To change default profile of aws cli the following construction is used
# session = boto3.Session(profile_name='my_user')
# client = session.client('codeartifact')

def list_packages(domain, domainOwner, repository, format):
    """Get list packages in CodeArtifact repository"""
    response = client.list_packages(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        maxResults=100)
    return response['packages']

def list_package_versions(domain, domainOwner, repository, format, namespace, package):
    """Get package versions in CodeArtifact repository"""
    response = client.list_package_versions(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        namespace=namespace,
        package=package,
        status=artifact_status_to_delete,
        sortBy='PUBLISHED_TIME',
        maxResults=100
    )
    return response["versions"]

def delete_package_versions(domain, domainOwner, repository, format, namespace, package, list_of_versions):
    """Delete package versions from CodeArtifact repository"""
    response = client.delete_package_versions(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        namespace=namespace,
        package=package,
        versions=list_of_versions,
        expectedStatus=artifact_status_to_delete
    )
    return response

def create_list_versions(list_of_versions):
    """Create a list of package versions available in CodeArtifact repository"""
    list_versions = [item['version'] for item in list_of_versions]
    return list_versions

for pkg in list_packages(domain_name,
                            domain_owner,
                            repository_name,
                            format_artifact):
    list_art_vers = list_package_versions(domain_name,
                                            domain_owner,
                                            repository_name,
                                            format_artifact,
                                            pkg['namespace'],
                                            pkg['package'])
    if len(list_art_vers) > 0:
        versions = create_list_versions(list_art_vers)
        print(f'Packages will be deleted: {pkg["namespace"]}:{pkg["package"]}: {versions}')
        delete_package_versions(domain_name,
                                domain_owner,
                                repository_name,
                                format_artifact,
                                pkg['namespace'],
                                pkg['package'],
                                versions)
    else:
        print(f'Nothing to delete for package: {pkg["namespace"]}:{pkg["package"]}')
