# test-websites

Purpose of repository is to enable developer to easily deploy test applications on ec2 instance. Deployed applications can be further tested for connection through nginx proxy server.

## docker compose
- **docker-compose-local.yml** - can be used for local deployment and tests. Remember to replace "***" with relevant information.
- **docker-compose.yml** - can be used for ec2 deployment and tests. Remember to replace "***" with relevant information.

- ENVIRONMETAL variables **LUNCH** and **GRADIO**, value "false" means that application will not be deployed.
- If you do not deploy all applications, check health check and remove "&&" sign and "curl --fail {url}" command.
- Applications are set to work for 10h after start, after that time applications stops running and docker exits. 

## cloud-init user data
- **cloud-init-test-websites.yml** - can be used as user data for ec2 instance. It installs test websites, using above docker-compose file. Remember to replace "***" with relevant information. Base used was Amazon 2023. AMI you use might require additional instalations as docker and docekr compose.