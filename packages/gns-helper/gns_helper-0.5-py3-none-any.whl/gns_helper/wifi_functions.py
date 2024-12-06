import os

def configure_wifi(ssid, password):
    """
    Configures the Wi-Fi settings on a system by adding the SSID and password to the wpa_supplicant configuration file.

    Parameters:
        ssid (str): The SSID (name) of the Wi-Fi network.
        password (str): The password for the Wi-Fi network.

    Functionality:
        - Prepares the necessary configuration lines for the wpa_supplicant file.
        - Grants write permissions to the wpa_supplicant configuration file.
        - Writes the Wi-Fi configuration to the file.
        - Triggers a refresh of the Wi-Fi settings to apply the changes.

    Notes:
        - The function assumes that the script has the necessary permissions to modify
          `/etc/wpa_supplicant/wpa_supplicant.conf`. If not, permissions must be granted manually.
        - The `sudo` commands used in this function might require passwordless sudo configuration
          for non-interactive execution.

    Example:
        configure_wifi("MyNetwork", "SecurePassword123")

    Output:
        Prints a confirmation message once the configuration is added and refreshed.
    """
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        'country=IN',
        '\n',
        'network={',
        '\tssid="{}"'.format(ssid),
        '\tpsk="{}"'.format(password),
        '}'
        ]
    config = '\n'.join(config_lines)
    
    #give access and writing. may have to do this manually beforehand
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
    
    #writing to file
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
    
    print("Wifi config added. Refreshing configs")
    ## refresh configs
    os.popen("sudo wpa_cli -i wlan0 reconfigure")

#if __name__ == '__main__':
#    configure_wifi("SARVESH", "home@run1")