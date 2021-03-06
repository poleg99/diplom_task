resource "aws_security_group" "worker_group_mgmt_one" {
  name_prefix = "worker_group_mgmt_one"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      var.vpc_cidr,
    ]
  }
}

resource "aws_security_group" "worker_group_mgmt_two" {
  name_prefix = "worker_group_mgmt_two"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "192.168.0.0/16",
    ]
  }
}

resource "aws_security_group" "all_worker_mgmt" {
  name_prefix = "all_worker_management"
  vpc_id      = module.vpc.vpc_id

  dynamic "ingress" {
    for_each = ["22", "80", "443"]
    content {
      description = "bunch of TCP ports for webservers"
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = [
        var.vpc_cidr,
        "172.16.0.0/12",
        "192.168.0.0/16",
      ]
    }
  }
  #  ingress {
  #    from_port = 22
  #    to_port   = 22
  #    protocol  = "tcp"

  #    cidr_blocks = [
  #      var.vpc_cidr,
  #      "172.16.0.0/12",
  #      "192.168.0.0/16",
  #    ]
  #  }
}

#-------------Create Security group for dbservers----------
resource "aws_security_group" "db_sg" {
  name        = "dbserver-sg"
  description = "security group for dbservers"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "port for mysql dbservers"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = ["${aws_security_group.all_worker_mgmt.id}"]
    cidr_blocks     = ["0.0.0.0/0"]
  }
  egress {
    description = "egress for dbservers"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = merge(var.tags, { Name = "${var.env}-dbservers_sg" })
}
