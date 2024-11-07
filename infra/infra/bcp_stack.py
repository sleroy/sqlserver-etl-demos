from aws_cdk import Stack, aws_ec2 as ec2, aws_iam as iam
from constructs import Construct

class BcpStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.vpc = vpc
        
        self.role = iam.Role(
            self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Define the user data script
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash",
            "# Set environment variable to accept EULA"
            "export ACCEPT_EULA='Y'"
            "# Update the system",
            "sudo yum update -y",
            "# Install EPEL repository",
            "sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm",
            "# Install the Microsoft repository RPM",
            "sudo curl -o /etc/yum.repos.d/msprod.repo https://packages.microsoft.com/config/rhel/8/prod.repo",
            "# Install the MSSQL tools (which includes BCP)",
            "sudo ACCEPT_EULA='Y' yum install -y mssql-tools unixODBC-devel",
            "# Add the tools to the PATH for all users",
            "echo 'export PATH=\"$PATH:/opt/mssql-tools/bin\"' | sudo tee /etc/profile.d/mssql-tools.sh",
            "# Make the script executable",
            "sudo chmod +x /etc/profile.d/mssql-tools.sh",
            "# Print BCP version to verify installation",
            "/opt/mssql-tools/bin/bcp -v"
        )        

        
        instance = ec2.Instance(
            self, "BCPSInstance",
            instance_type=ec2.InstanceType("m5.large"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            role=self.role,
            user_data=user_data
        )
        
    
