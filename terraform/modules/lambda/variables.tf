variable "region" {
  description = "The aws region to deploy resources"
  default     = "ap-northeast-2"
  type        = string
}

variable "account_id" {
  description = "aws account id"
}

variable "vpc_id" {
  description = "vpc id"
}

variable "subnet_ids" {
  description = "list of subnet ids within the vpc"
  type        = list(string)
}
