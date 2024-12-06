import ipaddress
from src import environment
from collections import defaultdict
from pynetbox import api as netbox_api


class NetBoxInstance(netbox_api):
    """
    This class extends the pynetbox api class by adding additional methods that are not strictly related to NetBox
    data itself, but more like custom methods that help a manage data within NetBox
    """
    def __init__(self, url=None, token=None):
        self.url = url or environment.get_netbox_url()
        self.token = token or environment.get_netbox_token()

        super(NetBoxInstance, self).__init__(url=self.url, token=self.token)

    def duplicated_device_serials(self):
        """
        Check if there are multiple devices with the same serial. This should not happen normally
        :return: The duplicated serial numbers
        """
        duplicates = []
        seen_values = defaultdict(list)

        for entry in [x for x in self.dcim.devices.all() if x.serial]:
            serial = entry['serial']
            if seen_values[serial]:
                duplicates.extend(seen_values[serial])
            else:
                seen_values[serial].append(entry['serial'])

        return duplicates

    def get_ip_addresses_without_prefix(self):
        """
        This function returns all IP addresses that have no associated prefix
        :return:
        """
        # Get prefixes and IP addresses from NetBox
        prefixes = [x.prefix for x in self.ipam.prefixes.all()]
        ip_addresses = [x.address for x in self.ipam.ip_addresses.all()]

        result = []
        # Loop through the IP addresses and check each one
        for ip_address in ip_addresses:
            # Get the corresponding network
            subnet = ipaddress.ip_network(ip_address, False)
            if str(subnet) not in prefixes:
                result.append(str(subnet))

        return result
