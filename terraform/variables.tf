variable "region" {
  description = "The aws region to deploy resources"
  default     = "ap-northeast-2"
  type        = string
}

variable "account_id" {
  description = "aws account id"
}

variable "account_key" {
  description = "aws account key"
  type        = string
}

variable "secret_key" {
  description = "aws secret key"
  type        = string
}

variable "subnet_prefix" {
  description = "cidr block for the subnet"
}

