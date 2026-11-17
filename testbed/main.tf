# Testbed sintético mínimo para validar o mapa
# Uso: terraform apply -var="prefix=horus-test"

variable "prefix" {
  default = "horus-test"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "${var.prefix}-vpc" }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  tags = { Name = "${var.prefix}-private" }
}

resource "aws_security_group" "app" {
  name   = "${var.prefix}-app-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}

resource "aws_security_group" "db" {
  name   = "${var.prefix}-db-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}

resource "aws_iam_role" "lambda" {
  name = "${var.prefix}-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" } }]
  })
}

resource "aws_lambda_function" "example" {
  function_name = "${var.prefix}-fn"
  role          = aws_iam_role.lambda.arn
  handler       = "index.handler"
  runtime       = "python3.12"
  filename      = "dummy.zip"
  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.app.id]
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "${var.prefix}-data-${random_id.suffix.hex}"
}

resource "random_id" "suffix" {
  byte_length = 4
}

output "vpc_id" { value = aws_vpc.main.id }
output "lambda_arn" { value = aws_lambda_function.example.arn }
output "s3_bucket" { value = aws_s3_bucket.data.bucket }
