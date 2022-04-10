variable "aws_region" {
  description = "Set AWS region where to start EC2 instances"
  type        = string
  default     = "us-west-2"
}

variable "k8s_name" {
  description = "Name for k8s cluster"
  type        = string
  default     = "k82EpamDiplom"
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
  default     = "t3.micro"
}

variable "tags" {
  description = "defaut tags"
  type        = map(any)
  default = {
    owner   = "Oleg Pavlov"
    project = "diplom-epam"
  }
}
