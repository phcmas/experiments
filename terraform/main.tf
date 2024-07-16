provider "aws" {
  region     = var.region
  access_key = var.account_key
  secret_key = var.secret_key
}

module "vpc" {
  source        = "./modules/vpc"
  subnet_prefix = var.subnet_prefix
}

module "lambda" {
  source     = "./modules/lambda"
  account_id = var.account_id
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.subnet_ids
}
