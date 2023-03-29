class ClusterResourceManager:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def remove_node(self, node_id):
        del self.nodes[node_id]

    def update_node_status(self, node_id, status):
        self.nodes[node_id].status = status

    def get_node_status(self, node_id):
        return self.nodes[node_id].status

    def get_all_nodes(self):
        return self.nodes.values()

    def get_available_node(self, resources_required):
        for node in self.nodes.values():
            if node.status == "active" and node.available_resources() >= resources_required:
                return node
        return None
