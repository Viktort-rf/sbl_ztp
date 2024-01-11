import os


nb_directory_path = os.path.join(os.path.dirname(__file__), "nb_render_cfg")

tftp_destination_directory = "/srv/tftp"
tftp_ip = "172.30.130.131"

username = "NOC"
password = "NOC"
vlan_id = "1555"

template_qsw_4610_init_cfg = "qsw_4610_init_cfg.j2"
soft_qsw_4610 = "8.2.1.186"

msk_devices_ip = "1.1.1.1"
msk_devices_mask = "2.2.2.2"
msk_devices_gw = "3.3.3.3"

ekb_devices_ip = "10.196.10.2"
ekb_devices_mask = "255.255.255.248"
ekb_devices_gw = "10.196.10.1"
