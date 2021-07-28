import boto3

client = boto3.client('codeartifact')

domain_name = 'test'
repository_name = 'test_repo'
format_artifact = 'maven'
domain_owner = '123456789123'
artifact_status_to_delete = 'Unlisted'

def list_packages(domain, domainOwner, repository, format):
    response = client.list_packages(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        maxResults=100)

    return response['packages']

def list_package_versions(domain, domainOwner, repository, format, namespace, package):
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
    
def delete_package_versions(domain, domainOwner, repository, format, namespace, package, list):
    response = client.delete_package_versions(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        namespace=namespace,
        package=package,
        versions=list,
        expectedStatus=artifact_status_to_delete
    )
    return response

def create_list_versions(list):
    list_versions = [item['version'] for item in list]

    return list_versions

for pkg in list_packages(domain_name, domain_owner, repository_name, format_artifact):
    list_art_vers = list_package_versions(domain_name, domain_owner, repository_name, format_artifact, pkg['namespace'], pkg['package'])
    if len(list_art_vers) > 0:
        versions = create_list_versions(list_art_vers)
        print(f'Packages will be deleted: {pkg["namespace"]}:{pkg["package"]}: {versions}')
        delete_package_versions(domain_name, domain_owner, repository_name, format_artifact, pkg['namespace'], pkg['package'], versions)
    else:
        print(f'Nothing to delete for package: {pkg["namespace"]}:{pkg["package"]}')
