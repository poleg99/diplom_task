# General

variable "aws_region" {
  description = "Set AWS region where to start EC2 instances"
  type        = string
  default     = "us-west-2"
}

variable "k8s_name" {
  description = "Name for k8s cluster"
  type        = string
  default     = "k8sEpamDiplom"
}

variable "env" {
  description = "Cluster environment"
  default     = "dev"
}

variable "server_size" {
  description = "Server instance type per environment"
  default = {
    prod    = "t3.medium"
    dev     = "t3.small"
    default = "t3.nano"
  }
}

variable "aws_instance_type" {
  description = "EC2 type"
  type        = string
  default     = "t3.small"
}

variable "tags" {
  description = "defaut tags"
  type        = map(any)
  default = {
    owner   = "Oleg Pavlov"
    project = "diplom-epam"
  }
}

# for VPC
variable "vpc_cidr" {
  default     = "10.20.0.0/16"
  description = "vpc subnet id"
}

variable "public_subnet_cidrs" {
  default = [
    "10.20.11.0/24",
    "10.20.12.0/24",
    "10.20.13.0/24"
  ]
  description = "public subnets cidr"
}

variable "private_subnet_cidrs" {
  default = [
    "10.20.31.0/24",
    "10.20.32.0/24",
    "10.20.33.0/24"
  ]
  description = "private subnets cidr"
}

# for Mysql
variable "db_server_size_prod" {
  description = "db type"
  type        = string
  default     = "db.t3.small"
}

variable "database_name_prod" {
  default     = "metalsdb"
  description = "database name"
}

variable "database_user_prod" {
  default     = "metalsdbuser"
  description = "database user for wordpress"
}

variable "database_password_prod" {
  default     = "Passw0rd123"
  description = "database pass for wordpress db"
}

variable "db_server_size_staging" {
  description = "db type"
  type        = string
  default     = "db.t3.small"
}

variable "database_name_staging" {
  default     = "metalsdb"
  description = "database name"
}

variable "database_user_staging" {
  default     = "metalsdbuser"
  description = "database user for wordpress"
}

variable "database_password_staging" {
  default     = "Passw0rd123"
  description = "database pass for wordpress db"
}
