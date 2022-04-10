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
  cidr                 = "10.20.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.20.11.0/24", "10.20.12.0/24", "10.20.13.0/24"]
  public_subnets       = ["10.20.31.0/24", "10.20.32.0/24", "10.20.33.0/24"]
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
