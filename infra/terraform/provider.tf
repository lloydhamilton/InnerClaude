terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.54.1"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.2"
    }
    tls = {
      source = "hashicorp/tls"
      version = "4.0.6"
    }
  }

  backend "s3" {
    bucket  = "innerclaude-tf-state"
    key     = "terraformstate/innerclaude/state"
    region  = "eu-west-2"
    encrypt = true
  }
}

provider "aws" {
  default_tags {
    tags = {
      "managed-by" = "terraform"
    }
  }
}