class Model():
    def __init__(self, model_dict):
        id, model_name, path, base_name = model_dict['id'], model_dict['name'], model_dict['path'], model_dict['base_name']
        self.id = id
        self.model_name = model_name
        self.path = path
        self.base_name = base_name

    def __str__(self):
        return "id: %s, model_name: %s, path: %s, base_name: %s" % (self.id, self.model_name, self.path, self.base_name)


    def to_dict(self):
        return {
            "id": self.id,
            "model_name": self.model_name,
            "path": self.path,
            "base_name": self.base_name
        }
        
