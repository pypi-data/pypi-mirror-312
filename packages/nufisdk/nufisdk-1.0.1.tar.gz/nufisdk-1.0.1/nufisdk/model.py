from datetime import datetime


class NpuDeploy:
    def __init__(self, name, namespace, creation_timestamp, replicas=1):
        self.name = name
        self.namespace = namespace
        self.creation_timestamp = datetime.strptime(
            creation_timestamp, "%Y-%m-%dT%H:%M:%SZ"
        )
        self.replicas = replicas

    def __str__(self):
        create_date = self.creation_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return f"Name: {self.name}, Namespace: {self.namespace}, Replicas: {self.replicas}, Created: {create_date}"


class DeployDetail:
    def __init__(
        self,
        name,
        namespace,
        image,
        cpu,
        memory,
        creation_timestamp,
        replicas,
        accelerator_type,
        accelerator_count,
        available_replicas,
        endpoint,
    ):
        self.name = name
        self.namespace = namespace
        self.image = image
        self.cpu = cpu
        self.memory = memory
        self.replicas = f"{available_replicas}/{replicas}"
        self.creation_timestamp = datetime.strptime(
            creation_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.accelerator_type = accelerator_type
        self.accelerator_count = accelerator_count
        self.endpoint = endpoint

    def __str__(self):
        create_date = self.creation_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return (
            f"Name: {self.name}, Namespace: {self.namespace}, Image: {self.image}, CPU: {self.cpu}, Memory: {self.memory}, "
            f"Replicas: {self.replicas}, Created: {create_date}"
        )
