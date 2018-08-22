import re
from utils import repository

full_version_regex = re.compile(r"^\d+\.\d+\.\d+$")
minor_version_regex = re.compile(r"(?:^(\d+)\.[xX]$)|(?:^\^(d+)\.\d+\.\d+$)")
patch_version_regex = re.compile(r"(?:^(\d+\.\d+)\.[xX]$)|(?:^\~(\d+\.\d+)\.\d+$)|(?:^(\d+\.\d+)$)")

def parse_package_string(package_string):
    if '@' in package_string:
        package_name, version = package_string.split('@')
        return {
            'name': package_name,
            'version': parse_semver(package_name, version)
        }
    else:
        return {
            'name': package_string,
            'version': parse_semver(package_string, 'latest')
        }


def parse_semver(package_name, semver):
    versions = repository.list_versions(package_name)

    if len(versions) == 0:
        raise ValueError('package {} has no deployed versions'.format(package_name))

    if semver == 'latest' or semver == '*' or semver == 'x':
        version = versions[0]
    elif full_version_regex.match(semver) and semver in versions:
        version = semver
    elif minor_version_regex.match(semver):
        major_version = minor_version_regex.search(semver).group(1)
        matched_versions = list(filter(lambda version: version.startswith('{}.'.format(major_version)), versions))
        if len(matched_versions) > 0:
            version = matched_versions[0]
    elif patch_version_regex.match(semver):
        major_and_minor_version = patch_version_regex.search(semver).group(1)
        matched_versions = list(filter(lambda version: version.startswith('{}.'.format(major_and_minor_version)), versions))
        if len(matched_versions) > 0:
            version = matched_versions[0]

    if not version:
        raise ValueError('{} is not a valid version'.format(semver))

    return version
