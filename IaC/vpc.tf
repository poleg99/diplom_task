provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "terraform-state-op"
    key    = "epam/diplom/terraform.tfstate"
    region = "us-west-2"
  }
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}

data "aws_availability_zones" "available" {}

module "vpc" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "3.2.0"
  name                 = "${var.k8s_name}-${var.env}-${random_string.suffix.result}"
  cidr                 = var.vpc_cidr
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = var.private_subnet_cidrs
  public_subnets       = var.public_subnet_cidrs
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  tags = merge(var.tags,
    {
      "kubernetes.io/cluster/${var.k8s_name}-${random_string.suffix.result}" = "shared"
  })

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.k8s_name}-${random_string.suffix.result}" = "shared"
    "kubernetes.io/role/elb"                                               = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.k8s_name}-${random_string.suffix.result}" = "shared"
    "kubernetes.io/role/internal-elb"                                      = "1"
  }
}
