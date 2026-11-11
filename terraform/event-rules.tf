# Regras de EventBridge para encaminhar eventos das contas-membro
# (incluir no StackSet ou aplicar via Terraform multi-account)

resource "aws_cloudwatch_event_rule" "config_changes" {
  name        = "horus-config-changes"
  description = "Forward Config and CloudTrail management events to central bus"
  event_pattern = jsonencode({
    source = [
      "aws.config",
      "aws.cloudtrail"
    ]
    detail-type = [
      "Config Configuration Item Change",
      "AWS API Call via CloudTrail"
    ]
  })
}

resource "aws_cloudwatch_event_target" "to_central" {
  rule      = aws_cloudwatch_event_rule.config_changes.name
  target_id = "central-bus"
  arn       = "arn:aws:events:${var.region}:${var.central_account_id}:event-bus/atlas-central-bus"
  role_arn  = aws_iam_role.eventbridge_forwarder.arn
}

resource "aws_iam_role" "eventbridge_forwarder" {
  name = "HorusEventBridgeForwarder"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "events.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}
