# allow ssh and http traffic
resource "aws_security_group" "allow_ssh_http" {
  name        = "AllowSSHHTTP"
  description = "Allow SSH and HTTP inbound traffic"
  vpc_id      = aws_vpc.main.id
}