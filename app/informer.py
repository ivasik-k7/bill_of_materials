from abc import ABC, abstractmethod

import requests


class PackageInfoInformer(ABC):
    @abstractmethod
    def request_info(
        self,
        package_name,
        package_version=None,
    ) -> dict | None:
        raise NotImplementedError("Method 'get_package_info' is not implemented!")


class PubPackageInfoInformer(PackageInfoInformer):
    def request_info(self, package_name, package_version=None) -> dict | None:
        url = f"https://pub.dev/api/packages/{package_name}"
        if package_version:
            url += f"/versions/{package_version}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class PyPackageInfoInformer(PackageInfoInformer):
    def request_info(self, package_name, package_version=None) -> dict | None:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if package_version:
                releases = data.get("releases", {})
                if package_version in releases:
                    return releases[package_version][0]
                else:
                    return None
            else:
                return data
        else:
            return None
