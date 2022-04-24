resource "random_string" "suffix" {
  length  = 8
  special = false
}

data "aws_availability_zones" "available" {}

locals {
  cluster_name = "${var.k8s_name}-${random_string.suffix.result}"
}

module "vpc" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "3.2.0"
  name                 = "${var.k8s_name}-vpc"
  cidr                 = var.vpc_cidr
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.20.31.0/24", "10.20.32.0/24", "10.20.33.0/24"]
  public_subnets       = ["10.20.11.0/24", "10.20.12.0/24", "10.20.13.0/24"]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}
