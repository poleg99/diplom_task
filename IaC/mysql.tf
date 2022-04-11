
#----------------Create DB subnet group---------------------
resource "aws_db_subnet_group" "db_myslq" {
  name       = "rds-for-mysql"
  subnet_ids = module.vpc.private_subnets
  tags       = merge(var.tags, { Name = "${var.env}-db-subnet" })
}
#------------Create MySQL dbserver------------------------
resource "aws_db_instance" "mysql" {
  allocated_storage       = 10
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = var.db_server_size
  db_subnet_group_name    = aws_db_subnet_group.db_myslq.id
  vpc_security_group_ids  = ["${aws_security_group.db_sg.id}"]
  db_name                 = var.database_name
  username                = var.database_user
  password                = var.database_password
  backup_retention_period = 1
  apply_immediately       = true
  skip_final_snapshot     = true
  multi_az                = true
}
