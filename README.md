# InnerClaude

InnerClaude is a streamlit based chat interface for Claude. 

## Process

rough notes

- [ ] Create a streamlit app
- [ ] Define terraform infrastructure
  - [ ] Create an EC2 instance with appropriate security groups
  - [ ] Create security group with ingress and egress rules. Egress rule is required for the instance to access the internet.
  - [ ] Create an ssh key pair for the instance
  - [ ] Create an IAM role for the instance
- [ ] Define a CI/CD pipeline
  - [ ] Configure OCID
  - [ ] Create a GitHub action to deploy the streamlit app to the EC2 instance
  - USE FARGATE?