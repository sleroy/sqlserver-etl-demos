#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.vpc_stack import VpcStack
from infra.efs_stack import EfsStack
from infra.sql_stack import SqlStack

app = cdk.App()

vpc_stack = VpcStack(app, "VpcStack",)
efs_stack = EfsStack(app, "EfsStack", vpc=vpc_stack.vpc)
sql_stack = SqlStack(app, "SqlStack", vpc=vpc_stack.vpc)

app.synth()
