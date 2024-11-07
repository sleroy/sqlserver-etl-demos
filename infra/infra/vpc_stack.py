from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct

class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        self.vpc = ec2.Vpc(self, "DemoVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Private",
                    cidr_mask=24
                )
            ],
            nat_gateways=1
        )

        # Add S3 Gateway Endpoint
        self.vpc.add_gateway_endpoint("S3Endpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3,
        )

        # Create SQL security group
        security_group = ec2.SecurityGroup(self, "SQLServerSG",
            vpc=self.vpc,
            description="Allow 1443 from anywhere",
            allow_all_outbound=True
        )

        # Add an ingress rule to allow SQL Server access
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(1443),
            description="Allow SQL Server access from anywhere"
        )
        
        