#!/usr/bin/env python3
"""Verify a deployed VPC and print a short report (uses boto3)."""
import argparse
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def tag(resource, key="Name"):
    for t in resource.get("Tags", []):
        if t["Key"] == key:
            return t["Value"]
    return "-"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vpc-id", required=True)
    p.add_argument("--region", default="ap-south-1")
    args = p.parse_args()

    ec2 = boto3.client("ec2", region_name=args.region)
    flt = [{"Name": "vpc-id", "Values": [args.vpc_id]}]

    try:
        vpc = ec2.describe_vpcs(VpcIds=[args.vpc_id])["Vpcs"][0]
        subnets = ec2.describe_subnets(Filters=flt)["Subnets"]
        igws = ec2.describe_internet_gateways(
            Filters=[{"Name": "attachment.vpc-id", "Values": [args.vpc_id]}]
        )["InternetGateways"]
        nats = ec2.describe_nat_gateways(Filters=flt)["NatGateways"]
        nats = [n for n in nats if n["State"] != "deleted"]
    except (BotoCoreError, ClientError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"VPC {vpc['VpcId']} ({tag(vpc)}) cidr={vpc['CidrBlock']} state={vpc['State']}")
    print(f"Internet gateways: {len(igws)}")
    print(f"NAT gateways: {len(nats)}")
    print(f"Subnets: {len(subnets)}")
    for s in sorted(subnets, key=lambda x: x["CidrBlock"]):
        kind = "public" if s["MapPublicIpOnLaunch"] else "private"
        print(f"  - {s['SubnetId']} {s['CidrBlock']:<16} {s['AvailabilityZone']:<14} {kind:<8} {tag(s)}")

    if not igws or not subnets:
        print("ERROR: VPC is missing an internet gateway or subnets", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
