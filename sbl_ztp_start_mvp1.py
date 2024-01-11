import shutil
import sys
from modules.qsw import qsw_4610_connect_and_copy_config, qsw_4610_connect_and_check_soft
from modules.gen_init_cfg import generate_config
from variables.sensitive import nb
from variables.static import os, username, password, nb_directory_path, tftp_destination_directory, tftp_ip, msk_devices_ip, msk_devices_mask, msk_devices_gw, ekb_devices_ip, ekb_devices_mask, ekb_devices_gw, vlan_id, template_qsw_4610_init_cfg, soft_qsw_4610


# Setup script work dir as current dir. This section for test
# script_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(script_dir)
# print('Current working directory:', os.getcwd())
# print('Path in virtual environment:', os.path.dirname(os.path.abspath(__file__)))


# Set region
while True:
    region = input('Please, input region (1, 2, 3, or 4) where start configure devices:\n1. MSK\n2. EKB\n3. SPB\n4. NSK\n')
    if region in ['1', '2', '3', '4']:
        break
    else:
        print('Invalid input. Please input 1, 2, 3, or 4.')

# Set name
name_device = input('Please, input device NAME: ').upper()

# Render config and init config. Then move to local tftp server
try:
    response = nb.dcim.devices.get(name=name_device).render_config.create()
    content_text = response.get('content', '')
    os.makedirs(nb_directory_path, exist_ok=True)
    devices = nb.dcim.devices.filter(name=name_device, status='active', has_primary_ip=True)
    for device in devices:
        device_type = device.device_type.slug
        
        # Get cfg format for qsw devices
        if device_type == 'qsw-4610-10t-poe-ac':
            nb_file_path = os.path.join(nb_directory_path, f'{name_device}_conf.cfg')
            with open(nb_file_path, 'w', encoding='utf-8') as file:
                file.write(content_text)
            print(f'\nRender config saved to {nb_file_path}\n')
            
            # Move file to local tftp
            try:
                if os.path.exists(nb_file_path):
                    shutil.copy2(nb_file_path, tftp_destination_directory)
                    print(f'File copied from {nb_file_path} to {tftp_destination_directory}\n')
                else:
                    print(f'File {nb_file_path} does not exist.\n')
            except Exception as e:
                print(f'ERROR for copying file to local tftp: {e}\n')

            # Get init cfg per region
            # MSK
            if region == '1':
                config = generate_config(template_qsw_4610_init_cfg, username, password, vlan_id, msk_devices_ip, msk_devices_mask, msk_devices_gw)
                print(config)
                wait_user = input('Waiting for the user init conf to be configured. After conf, please input ENTER...')
                qsw_4610_connect_and_check_soft(msk_devices_ip, username, password, soft_qsw_4610)
                wait_user = input('Waiting for the user read informations. After end, please ENTER...')
                qsw_4610_connect_and_copy_config(msk_devices_ip, username, password, tftp_ip, name_device)

            # EKB
            if region == '2':
                config = generate_config(template_qsw_4610_init_cfg, username, password, vlan_id, ekb_devices_ip, ekb_devices_mask, ekb_devices_gw)
                print(config)
                wait_user = input('Waiting for the user init conf to be configured. After conf, please input ENTER...')
                qsw_4610_connect_and_check_soft(ekb_devices_ip, username, password, soft_qsw_4610)
                wait_user = input('Waiting for the user read informations. After end, please ENTER...')
                qsw_4610_connect_and_copy_config(ekb_devices_ip, username, password, tftp_ip, name_device)
        else:
            print(f'Current device model ({device_type}) not found in script.')
except Exception as e:
    print(f'\nFailed to retrieve render config. Exception: {e}\n')
    sys.exit()
