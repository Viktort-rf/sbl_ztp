from jinja2 import Environment, FileSystemLoader

def generate_config(template_path, username, password, vlan_id, ip_address, subnet_mask, gateway):
    template_env = Environment(loader=FileSystemLoader('templates/qsw'))
    template = template_env.get_template(template_path)

    config = template.render(
        username=username,
        password=password,
        vlan_id=vlan_id,
        ip_address=ip_address,
        subnet_mask=subnet_mask,
        gateway=gateway
    )

    return config