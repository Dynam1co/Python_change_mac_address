import subprocess
import optparse
import re
import os


def get_current_mac(interface):
    ifconfig = subprocess.check_output(['ifconfig', interface])
    mac_address = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig))

    if mac_address:
        return mac_address.group(0)

    raise Exception('Sorry, MAC address not found')


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC addr')
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC addr')

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error('[!] Please specify an interface, use --help for more info.')
    elif not options.new_mac:
        parser.error('[!] Please specify a MAC, use --help for more info.')

    return options


def change_mac(interface, new_mac):
    print('Changing MAC address form {} to {}'.format(interface, new_mac))
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])


def down_interface(interface):
    print('Turning off network interface: {}'.format(interface))
    subprocess.call(['ifconfig', interface, 'down'])


def up_interface(interface):
    print('Turning on network interface: {}'.format(interface))
    subprocess.call(['ifconfig', interface, 'up'])


if __name__ == "__main__":
    if os.geteuid() == 0:  # Check super user
        options = get_arguments()
        current_mac = get_current_mac(options.interface)

        down_interface(options.interface)

        print('Current MAC: {}'.format(current_mac))
        change_mac(options.interface, options.new_mac)

        up_interface(options.interface)

        if current_mac != options.new_mac:
            print('MAC address was succesfully changed to {}'.format(options.new_mac))
        else:
            raise Exception('It was not possible to change the MAC address')
    else:
        raise Exception('Pemission denied')
