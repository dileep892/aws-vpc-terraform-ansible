# aws-vpc-terraform-ansible

Deploy an AWS VPC with **Terraform**, orchestrated by **Ansible** playbooks, with a **Python (boto3)** verification step.

## What gets created

- VPC with DNS support/hostnames enabled
- Public and private subnets across `az_count` availability zones
- Internet Gateway, public route table
- Optional single NAT Gateway + Elastic IP, private route table
- Optional EKS/Kubernetes subnet tags (set `eks_cluster_name`), so you can run EKS in this VPC later

## Layout

```
terraform/   main.tf variables.tf outputs.tf versions.tf terraform.tfvars.example
ansible/     deploy_vpc.yml destroy_vpc.yml ansible.cfg collections-requirements.yml
scripts/     vpc_info.py
requirements.txt
```

## Prerequisites

- Terraform >= 1.5
- Python 3.9+
- AWS credentials with permission to manage VPC/EC2 networking

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r ansible/collections-requirements.yml

export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
# or: export AWS_PROFILE=myprofile
```

## Deploy

```bash
cd ansible
ansible-playbook deploy_vpc.yml -e plan_only=true      # preview
ansible-playbook deploy_vpc.yml                        # apply
ansible-playbook deploy_vpc.yml -e project_name=prod -e vpc_cidr=10.20.0.0/16 -e aws_region=us-east-1
ansible-playbook deploy_vpc.yml -e eks_cluster_name=my-eks   # add Kubernetes subnet tags
```

## Destroy

```bash
ansible-playbook destroy_vpc.yml -e confirm_destroy=yes
```

## Notes

- NAT Gateways cost money per hour plus data processing. Set `-e enable_nat_gateway=false` for testing.
- State is local by default. For teams, add an S3 + DynamoDB backend in `terraform/versions.tf`.
- Pass the same `project_name` and `aws_region` to destroy that you used to deploy.
- Never commit `terraform.tfvars`, state files or credentials.
