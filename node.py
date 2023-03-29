class Node:
    def __init__(self, node_id, total_resources):
        self.node_id = node_id
        self.total_resources = total_resources
        self.used_resources = 0
        self.status = "active"

    def available_resources(self):
        return self.total_resources - self.used_resources

    def allocate_resources(self, resources):
        self.used_resources += resources

    def release_resources(self, resources):
        self.used_resources -= resources
