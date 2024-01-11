from netmiko import ConnectHandler
import re

def qsw_4610_connect_and_copy_config(devices_ip, username, password, tftp_ip, name_device):
    try:
        device_info = {
            'device_type': 'cisco_xe',
            'ip': str(devices_ip),
            'username': username,
            'password': password,
            # 'read_timeout_override': 30,
            # 'session_log': 'qsw_4610_connect_and_copy_config.txt'
            }
        net_connect = ConnectHandler(**device_info)
        print(f'Connect to device {devices_ip}\n')

        copy_cfg = net_connect.send_command_timing(f'copy tftp://{tftp_ip}/{name_device}_conf.cfg {name_device}_conf.cfg', delay_factor=10)

        if 'Write ok.' in copy_cfg:
            print('Success download from tftp\n')
            net_connect.send_command(f'boot startup-config {name_device}_conf.cfg')
            check_boot = net_connect.send_command('show boot-files | i startup.*next')

            if f'{name_device}_conf.cfg' in check_boot:
                print('Success set boot-startup-cfg')
                reload_device = net_connect.send_command_timing('reload')
                reload_device += net_connect.send_command_timing('Y')
            else:
                print('ERROR set boot-startup-cfg')
                net_connect.disconnect()

        elif 'Confirm to overwrite the existed destination file?' in copy_cfg:
            copy_cfg += net_connect.send_command_timing('Y')
            print('Overwrite the existed destination file\n')
            net_connect.send_command(f'boot startup-config {name_device}_conf.cfg')
            check_boot = net_connect.send_command('show boot-files | i startup.*next')
            
            if f'{name_device}_conf.cfg' in check_boot:
                print('Success set boot-startup-cfg')
                reload_device = net_connect.send_command_timing('reload')
                reload_device += net_connect.send_command_timing('Y')
            else:
                print('ERROR set boot-startup-cfg')
                net_connect.disconnect()

        else:
            print('There was an issue with the copy operation.\n')
            net_connect.disconnect()

    except Exception as e:
        print(f'Failed to connect to device {devices_ip}. Exception: {e}\n')

def qsw_4610_connect_and_check_soft(devices_ip, username, password, soft_qsw_4610):
    try:
        device_info = {
            'device_type': 'cisco_xe',
            'ip': str(devices_ip),
            'username': username,
            'password': password,
            # 'read_timeout_override': 30,
            # 'session_log': 'qsw_4610_connect_and_check_soft.txt'
            }
        net_connect = ConnectHandler(**device_info)
        print(f'Connect to device {devices_ip}\n')

        check_soft_qsw = net_connect.send_command('show version | i SoftWare Version')
        if soft_qsw_4610 not in check_soft_qsw:
            match_ver = re.search(r'\d+\.\d+\.\d+\.\d+', check_soft_qsw).group()
            print(f'!!!The software is not targeted on the device. Need manual check and upgrade!!!\nTarget soft - {soft_qsw_4610}\nDevice soft - {match_ver}\nThis manual:\nhttps://ftp.qtech.ru/Switch/Access/QSW-4610/Firmware\n')
        net_connect.disconnect()

    except Exception as e:
        print(f'Failed to connect to device {devices_ip}. Exception: {e}\n')
