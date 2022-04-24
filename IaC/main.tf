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
