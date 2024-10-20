# RSA key of size 4096 bits
resource "tls_private_key" "rsa_4096" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "key_pair" {
  public_key = tls_private_key.rsa_4096.public_key_openssh
  key_name   = "${var.app_name}_instance_key_pair"
}

resource "aws_secretsmanager_secret" "key_pair_secret" {
  name = "${var.app_name}_instance_key_pair"
}

resource "aws_secretsmanager_secret_version" "key_pair_secret_version" {
  secret_id     = aws_secretsmanager_secret.key_pair_secret.id
  secret_string = tls_private_key.rsa_4096.private_key_pem
}