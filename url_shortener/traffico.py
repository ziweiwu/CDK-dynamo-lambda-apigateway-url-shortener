from aws_cdk import core, aws_ec2, aws_ecs
from aws_cdk.core import Construct


class Traffico(Construct):

    def __init__(self, scope: Construct, id: str, url: str, tps: int):
        super().__init__(scope, id)

        cluster = aws_ecs.Cluster(self, 'Cluster')

        taskdef = aws_ecs.FargateTaskDefinition(self, 'PingerTask')
        taskdef.add_container("Pinger", image=aws_ecs.ContainerImage.from_asset('./pinger'), environment={
            'URL': url
        })

        # since each container generate 1 tps to url, we can adjust desired tps by using desire container count
        aws_ecs.FargateService(
            self, 'PingerService', cluster=cluster, task_definition=taskdef, desired_count=tps)
