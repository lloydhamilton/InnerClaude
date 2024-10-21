resource "aws_instance" "docker_instance" {
  ami           = "ami-03c6b308140d10488"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  key_name      = aws_key_pair.key_pair.key_name
  user_data     = file("user_data.sh")
  security_groups = [aws_security_group.allow_ssh_http_default.name]
  tags = {
    Name = "${var.app_name}_docker_instance"
  }
}

