import requests
import CloudFlare
import os
import sys
import click

def get_ip():
    return requests.get("https://ifconfig.me").text

def update_record(zone, subdomain, ip):
    # data init
    zone_params = {
        "name": zone
    }

    search_params = {
        "name": subdomain
    }

    new_record_data = {
        "name": subdomain,
        "type": "A",
        "content": ip
    }

    # logic
    cf = CloudFlare.CloudFlare()
    zone_id = cf.zones.get(params=zone_params)[0]["id"]
    records = cf.zones.dns_records.get(zone_id, params=search_params)
    if not records:
        cf.zones.dns_records.post(zone_id, data=new_record_data)
        print("New record created")
    else:
        record_id = records[0]["id"]
        if ip != records[0]["content"]:
            cf.zones.dns_records.put(zone_id, record_id, data=new_record_data)
            print("Record updated")
        else:
            print("No need to update")

@click.command()
@click.argument("subdomain")
@click.option("-i", "--ip", type=str, default=get_ip(), show_default="public IP", help="Specify record IP")
def main(subdomain, ip):
    zone = ".".join(subdomain.split(".")[-2:])
    update_record(zone, subdomain, ip)
