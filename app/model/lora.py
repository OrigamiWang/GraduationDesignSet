class Lora():
    def __init__(self, lora_dict):
        id, lora_name, path, base_name = lora_dict['id'], lora_dict['name'], lora_dict['path'], lora_dict['base_name']
        self.id = id
        self.lora_name = lora_name
        self.path = path
        self.base_name = base_name

    def __str__(self):
        return "id: %s, lora_name: %s, path: %s, base_name: %s" % (self.id, self.lora_name, self.path, self.base_name)


    def to_dict(self):
        return {
            "id": self.id,
            "lora_name": self.lora_name,
            "path": self.path,
            "base_name": self.base_name
        }
        
