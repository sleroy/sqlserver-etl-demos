from aws_cdk import Stack, aws_ec2 as ec2, aws_iam as iam, aws_secretsmanager as secretsmanager
from constructs import Construct

class SqlStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.vpc = vpc
        self.role = iam.Role(
            self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        
        # Create SQL security group
        security_group = ec2.SecurityGroup(
            self, "SQLServerSG",
            vpc=self.vpc,
            description="Allow 1433 from anywhere",
            allow_all_outbound=True
        )
        
        # Add an ingress rule to allow SQL Server access
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(1433),
            description="Allow SQL Server access from anywhere"
        )
        
        password_secret = secretsmanager.Secret(
            self, "SQLServerInstancePassword",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                password_length=16,
                exclude_punctuation=True
            )
        )
        
        user_data = ec2.UserData.for_windows()
        user_data.add_commands(
            f'''
            <powershell>
            $password = (Get-SECSecretValue -SecretId {password_secret.secret_arn}).SecretString
            $password = ConvertTo-SecureString -String $password -AsPlainText -Force
            Set-LocalUser -Name 'Administrator' -Password $password
            </powershell>
            '''
        )
        
        instance = ec2.Instance(
            self, "SQLServerInstance",
            instance_type=ec2.InstanceType("m5.large"),
            machine_image=ec2.WindowsImage(ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_SQL_2019_STANDARD),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_group=security_group,
            role=self.role,
            user_data=user_data
        )
        
        password_secret.grant_read(instance.role)
    
