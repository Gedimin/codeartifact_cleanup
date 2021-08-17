#!/usr/bin/env python
# encoding: utf-8

import os
import boto3
from dotenv import load_dotenv


def get_list_packages(client, domain, domainOwner, repository, format):
    """Get list packages in CodeArtifact repository"""
    response = client.list_packages(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        maxResults=100
    )
    return response['packages']

def get_list_package_versions(client, domain, domainOwner, repository, format, namespace, package, status):
    """Get package versions in CodeArtifact repository"""
    response = client.list_package_versions(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        namespace=namespace,
        package=package,
        status=status,
        sortBy='PUBLISHED_TIME',
        maxResults=100
    )
    return response["versions"]

def delete_package_versions(client, domain, domainOwner, repository, format, namespace, package, list_of_versions):
    """Delete package versions from CodeArtifact repository"""
    response = client.delete_package_versions(
        domain=domain,
        domainOwner=domainOwner,
        repository=repository,
        format=format,
        namespace=namespace,
        package=package,
        versions=list_of_versions
    )
    return response

def create_list_versions(list_of_versions):
    """Create a list of package versions available in CodeArtifact repository"""
    list_versions = [item['version'] for item in list_of_versions]
    return list_versions

def main():

    load_dotenv()

    domain_name = os.environ['domain_name']
    repository_name = os.environ['repository_name']
    format_artifact = os.environ['format_artifact']
    domain_owner = os.environ['domain_owner']
    artifact_status_to_delete = os.environ['artifact_status_to_delete']

    # # By default boto3 uses default profile of aws cli credentials
    # client_context = boto3.client('codeartifact')

    #  To change default profile of aws cli the following construction is used
    session = boto3.Session(profile_name='my_user')
    client_context = session.client('codeartifact')

    list_packages = get_list_packages(client=client_context,
                                        domain=domain_name,
                                        domainOwner=domain_owner,
                                        repository=repository_name,
                                        format=format_artifact)

    for pkg in list_packages:
        list_package_versions = get_list_package_versions(client=client_context,
                                                            domain=domain_name,
                                                            domainOwner=domain_owner,
                                                            repository=repository_name,
                                                            format=format_artifact,
                                                            namespace=pkg['namespace'],
                                                            package=pkg['package'],
                                                            status=artifact_status_to_delete)
        if len(list_package_versions) > 0:
            list_versions = create_list_versions(list_package_versions)
            print(f'Packages will be deleted: {pkg["namespace"]}:{pkg["package"]}: {list_versions}')

            delete_package_versions(client=client_context,
                                    domain=domain_name,
                                    domainOwner=domain_owner,
                                    repository=repository_name,
                                    format=format_artifact,
                                    namespace=pkg['namespace'],
                                    package=pkg['package'],
                                    list_of_versions=list_versions)
        else:
            print(f'Nothing to delete for package: {pkg["namespace"]}:{pkg["package"]}')

if __name__ == '__main__':
    main()
