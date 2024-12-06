import configparser
from pathlib import Path
from deltalake_tools.result import Result, Ok, Err

import logging

logging.getLogger('botocore.credentials').setLevel(logging.WARNING)

def load_aws_profile_config(profile_name: str) -> Result[tuple[str, str], Err]:
    """Load custom configurations like endpoint_url and addressing_style from AWS config."""
    aws_config_path = Path.home() / ".aws" / "config"
    config = configparser.ConfigParser()

    if not aws_config_path.exists():
        return Err(f"{aws_config_path} not found")

    config.read(aws_config_path)

    profile_section = f"profile {profile_name}"

    if profile_section not in config:
        return Err(f"Profile {profile_name} not found in {aws_config_path}")

    service_key = config.get(profile_section, "services", fallback=None)
    if not service_key:
        return Err(f"No services defined for profile {profile_name}")

    service_section = f"services {service_key}"
    if service_section not in config:
        return Err(f"Service {service_key} not found for profile {profile_name}")
    
    service_config = {}
    for key, value in config.items(service_section):
        if key.startswith("s3"):
            values = value.strip().splitlines()
            for val in values:
                vs = val.split("=")
                if len(vs) != 2:
                    continue
                clean_key = vs[0].strip()
                v = vs[1].strip()
                service_config[clean_key] = v

    endpoint_url = service_config.get("endpoint_url", None)
    addressing_style = service_config.get("addressing_style", "virtual")

    return Ok((endpoint_url, addressing_style))