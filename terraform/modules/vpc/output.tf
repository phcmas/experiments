output "server_private_ip" {
  value = aws_instance.web_server_instance.private_ip
}

output "server_id" {
  value = aws_instance.web_server_instance.id
}

output "vpc_id" {
  value = aws_vpc.prod_vpc.id
}

output "subnet_ids" {
  value = [aws_subnet.subnet_1.id]
}

