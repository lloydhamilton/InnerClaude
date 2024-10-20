resource "aws_instance" "docker_instance" {
  ami           = "ami-050d18b7ba1dcf9ab"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  key_name      = aws_key_pair.key_pair.key_name
  user_data     = file("user_data.sh")
}

