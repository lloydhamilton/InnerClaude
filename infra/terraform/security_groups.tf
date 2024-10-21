# allow ssh and http traffic
resource "aws_security_group" "allow_ssh_http" {
  name        = "AllowSSHHTTP"
  description = "Allow SSH and HTTP inbound traffic"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group_rule" "allow_ssh" {
  security_group_id = aws_security_group.allow_ssh_http.id
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = [aws_vpc.main.cidr_block]
}

# Security group fro default VPC.

resource "aws_security_group" "allow_ssh_http_default" {
  name        = "AllowSSHHTTP"
  description = "Allow SSH and HTTP inbound traffic"
  vpc_id      = "vpc-07ba8e3835fce3f8b"
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_default" {
  security_group_id = aws_security_group.allow_ssh_http_default.id
  from_port         = 22
  to_port           = 22
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}

data "aws_ec2_managed_prefix_list" "instance_connect" {
  name = "com.amazonaws.eu-west-2.ec2-instance-connect"
}

resource "aws_vpc_security_group_ingress_rule" "allow_instance_connect" {
  security_group_id = aws_security_group.allow_ssh_http_default.id
  from_port         = 22
  to_port           = 22
  ip_protocol       = "tcp"
  prefix_list_id    = data.aws_ec2_managed_prefix_list.instance_connect.id
}

resource "aws_vpc_security_group_egress_rule" "allow_egress" {
  security_group_id = aws_security_group.allow_ssh_http_default.id
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_cognito_user_pool" "example" {
  name = "${var.app_name}_cognito_user_pool"

  schema {
    name                     = "terraform"
    attribute_data_type      = "Boolean"
    mutable                  = false
    required                 = false
    developer_only_attribute = false
  }
}