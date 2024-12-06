from src import environment
from mydict import MyDict
from netmiko import ConnectHandler


class CiscoSSHDevice(object):
    """
    This class defines methods for fetching data from a Cisco device using NetMiko
    """
    def __init__(self, hostname, username=None, password=None):
        if not hostname:
            raise ValueError("Hostname is mandatory")

        self.hostname = hostname
        # Username and passwords can be provided as parameters (preferred) or as environment variables
        self.username = username or environment.get_cisco_username()
        self.password = password or environment.get_cisco_password()

        if environment.VERBOSE:
            print(f"Cisco username: {self.username}")

        netmiko_device = {
            'device_type': "cisco_ios",
            'ip': self.hostname,
            'username': self.username,
            'password': self.password,
            'secret': self.password
        }
        self.conn = ConnectHandler(**netmiko_device)

    def execute_command(self, command, parse=True):
        """
        This method executes a command on Cisco CLI and returns the result
        :param command: The command to run
        :param parse: Parse the output with textfsm (True)
        :return:
        """
        if parse:
            return self.conn.send_command(command, use_textfsm=True)

        return self.conn.send_command(command)

    def get_interface_details(self):
        """
        This method executes the 'show interface' command and returns the result parsed with textfsm
        :return:
        """
        interfaces = self.execute_command('show interface')
        return [MyDict(x) for x in interfaces]

    def get_device_serial(self):
        """
        This method gets the serial number of a device
        :return:
        """
        serial = self.conn.send_command('show version | include Processor')
        return serial.split(' ')[-1]
