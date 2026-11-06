# Event rules example for member accounts (include in StackSet)

# CloudTrail management events → central bus
# Config configuration item changes → central bus

# See AWS docs for exact event patterns.
# Example pattern for resource changes:
# {
#   "source": ["aws.ec2", "aws.lambda", "aws.s3", "aws.rds", "aws.eks", ...],
#   "detail-type": ["AWS API Call via CloudTrail", "Config Configuration Item Change"]
# }
