provider "aws" {
  region     = "ap-northeast-2"
  # access_key = ""
  # secret_key = ""
}


variable "subnet_prefix" {
  description = "cidr block for the subnet"
  default     = "10.0.66.0/24"
  # type        = string
}

# 1. create vpc
resource "aws_vpc" "prod_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "production"
  }
}

# 2. create internet gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.prod_vpc.id

  tags = {
    Name = "production"
  }
}

# 3. create custom route table
resource "aws_route_table" "prod_route_table" {
  vpc_id = aws_vpc.prod_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "production"
  }
}

# 4. create a subnet
resource "aws_subnet" "subnet_1" {
  vpc_id            = aws_vpc.prod_vpc.id
  cidr_block        = var.subnet_prefix[0].cidr_block
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = var.subnet_prefix[0].name
  }
}


# 5. associate subnet with route table
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet_1.id
  route_table_id = aws_route_table.prod_route_table.id
}


# 6. create security group to allow port 22,80,443
resource "aws_security_group" "allow_web" {
  name        = "allow_web_traffic"
  description = "allow web inbound traffic"
  vpc_id      = aws_vpc.prod_vpc.id

  ingress {
    description = "https"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "http"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "ssh"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_web"
  }
}

# 7. create a newtwork interface with an ip in the subnet that was created in step 4
resource "aws_network_interface" "web_server_nic" {
  subnet_id       = aws_subnet.subnet_1.id
  private_ips     = ["10.0.1.50"]
  security_groups = [aws_security_group.allow_web.id]
}

# 8. assign an elastic ip to the network interface created in step 7
resource "aws_eip" "one" {
  domain                    = "vpc"
  network_interface         = aws_network_interface.web_server_nic.id
  associate_with_private_ip = "10.0.1.50"
  depends_on                = [aws_internet_gateway.gw]
}

output "server_public_ip" {
  value = aws_eip.one.public_ip
}

# 9. create ubuntu server and install/enable apache2
resource "aws_instance" "web_server_instance" {
  ami               = "ami-062cf18d655c0b1e8"
  instance_type     = "t2.micro"
  availability_zone = "ap-northeast-2a"
  key_name          = "main-key"

  network_interface {
    network_interface_id = aws_network_interface.web_server_nic.id
    device_index         = 0
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install nginx -y
              sudo systemctl start nginx
              sudo systemctl enable nginx
              sudo ufw allow 'Nginx HTTP'
              sudo ufw enable
              EOF

  tags = {
    Name = "web-server"
  }
}

output "server_private_ip" {
  value = aws_instance.web_server_instance.private_ip
}

output "server_id" {
  value = aws_instance.web_server_instance.id
}






