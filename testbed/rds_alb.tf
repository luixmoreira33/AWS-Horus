# Expansão do testbed: RDS + ALB

resource "aws_db_subnet_group" "main" {
  name       = "${var.prefix}-db-subnet"
  subnet_ids = [aws_subnet.private.id]
}

resource "aws_db_instance" "example" {
  identifier           = "${var.prefix}-db"
  engine               = "postgres"
  engine_version       = "16"
  instance_class       = "db.t4g.micro"
  allocated_storage    = 20
  db_name              = "testdb"
  username             = "admin"
  password             = "ChangeMe123!"
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot  = true
  publicly_accessible  = false
}

resource "aws_lb" "app" {
  name               = "${var.prefix}-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.app.id]
  subnets            = [aws_subnet.private.id]
}

resource "aws_lb_target_group" "lambda" {
  name     = "${var.prefix}-tg"
  port     = 443
  protocol = "HTTPS"
  vpc_id   = aws_vpc.main.id
  target_type = "lambda"
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate.example.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.lambda.arn
  }
}

resource "aws_acm_certificate" "example" {
  domain_name       = "example.com"
  validation_method = "DNS"
}

output "rds_arn" { value = aws_db_instance.example.arn }
output "alb_arn" { value = aws_lb.app.arn }
