from aws_cdk import core
from traffico import Traffico


class TrafficStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        Traffico(self, 'TestTraffic',
                 url="https://09d3aqkv89.execute-api.us-east-1.amazonaws.com/prod",
                 tps=100)