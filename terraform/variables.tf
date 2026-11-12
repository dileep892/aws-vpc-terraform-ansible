variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "demo"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "az_count" {
  description = "Number of availability zones to use"
  type        = number
  default     = 2
}

variable "enable_nat_gateway" {
  description = "Create a single NAT gateway so private subnets have outbound internet"
  type        = bool
  default     = true
}

variable "eks_cluster_name" {
  description = "Optional. If set, subnets get the Kubernetes/EKS discovery tags"
  type        = string
  default     = ""
}
