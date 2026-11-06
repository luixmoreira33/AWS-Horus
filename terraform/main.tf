# Terraform principal - Conta central
# Premissas: Neptune, ECS Fargate, SQS, EventBridge bus, S3+CloudFront

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" { default = "us-east-1" }
variable "central_account_id" { type = string }
variable "external_id" { type = string description = "Strong random ExternalId" }
variable "org_id" { type = string default = "" }

# Event bus central
resource "aws_cloudwatch_event_bus" "atlas" {
  name = "atlas-central-bus"
}

# SQS para workers
resource "aws_sqs_queue" "atlas_events" {
  name                      = "atlas-events"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 1209600
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.atlas_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "atlas_dlq" {
  name = "atlas-events-dlq"
}

# Policy allowing member accounts to put events (example - restrict further)
resource "aws_cloudwatch_event_bus_policy" "atlas" {
  event_bus_name = aws_cloudwatch_event_bus.atlas.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowOrgPutEvents"
      Effect    = "Allow"
      Principal = "*"
      Action    = "events:PutEvents"
      Resource  = aws_cloudwatch_event_bus.atlas.arn
      Condition = {
        StringEquals = {
          "aws:PrincipalOrgID" = var.org_id
        }
      }
    }]
  })
}

# Neptune cluster (simplified - adjust instance class)
resource "aws_neptune_cluster" "atlas" {
  cluster_identifier                  = "atlas-graph"
  engine                              = "neptune"
  engine_version                      = "1.3.2.0" # check latest
  backup_retention_period             = 7
  preferred_backup_window             = "07:00-09:00"
  skip_final_snapshot                 = true
  iam_database_authentication_enabled = true
  # vpc_security_group_ids, subnet_group, etc. - add for production
}

resource "aws_neptune_cluster_instance" "atlas" {
  count              = 1
  cluster_identifier = aws_neptune_cluster.atlas.id
  engine             = "neptune"
  instance_class     = "db.r6g.large"
  apply_immediately  = true
}

# Role for workers (to assume AtlasReadOnly in members + access Neptune)
resource "aws_iam_role" "atlas_worker" {
  name = "AtlasWorkerRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "atlas_worker" {
  name = "AtlasWorkerPolicy"
  role = aws_iam_role.atlas_worker.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["sts:AssumeRole"]
        Resource = "arn:aws:iam::*:role/AtlasReadOnly"
        Condition = {
          StringEquals = { "sts:ExternalId" = var.external_id }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "neptune-db:*",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "events:PutEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

# Placeholder for ECS cluster, task def, service, ALB, S3 frontend bucket, etc.
# Expand in production.

output "event_bus_arn" { value = aws_cloudwatch_event_bus.atlas.arn }
output "sqs_url" { value = aws_sqs_queue.atlas_events.url }
output "neptune_endpoint" { value = aws_neptune_cluster.atlas.endpoint }
output "worker_role_arn" { value = aws_iam_role.atlas_worker.arn }
