
#----------------Create DB subnet group---------------------
resource "aws_db_subnet_group" "db_myslq" {
  name       = "rds-for-mysql"
  subnet_ids = module.vpc.private_subnets
  tags       = merge(var.tags, { Name = "mysql-db-subnet" })
}
#------------Create MySQL dbserver------------------------
resource "aws_db_instance" "mysql_staging" {
  allocated_storage       = 10
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = var.db_server_size_staging
  db_subnet_group_name    = aws_db_subnet_group.db_myslq.id
  vpc_security_group_ids  = ["${aws_security_group.db_sg.id}"]
  db_name                 = var.database_name_staging
  username                = var.database_user_staging
  password                = var.database_password_staging
  backup_retention_period = 1
  apply_immediately       = true
  skip_final_snapshot     = true
  multi_az                = true
}

resource "aws_db_instance" "mysql_prod" {
  allocated_storage       = 10
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = var.db_server_size_prod
  db_subnet_group_name    = aws_db_subnet_group.db_myslq.id
  vpc_security_group_ids  = ["${aws_security_group.db_sg.id}"]
  db_name                 = var.database_name_prod
  username                = var.database_user_prod
  password                = var.database_password_prod
  backup_retention_period = 1
  apply_immediately       = true
  skip_final_snapshot     = true
  multi_az                = true
}
