from aws_cdk import Stack, aws_ec2 as ec2, aws_efs as efs
from constructs import Construct

class EfsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create or use an existing VPC
        self.vpc = vpc

        # Create a security group for EFS
        efs_security_group = ec2.SecurityGroup(self, "EFSSecurityGroup",
            vpc=self.vpc,
            description="Security group for EFS",
            allow_all_outbound=True
        )

        # Allow inbound NFS traffic on port 2049 from within the same security group
        efs_security_group.add_ingress_rule(
            peer=efs_security_group,
            connection=ec2.Port.tcp(2049),
            description="Allow NFS traffic within the security group"
        )

        # Create the EFS file system
        file_system = efs.FileSystem(self, "DemoEFS",
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_group=efs_security_group,
            encrypted=True,
            lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING
        )
