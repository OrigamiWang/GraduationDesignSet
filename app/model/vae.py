class Vae():
    def __init__(self, vae_dict):
        id, vae_name, path, base_name = vae_dict['id'], vae_dict['name'], vae_dict['path'], vae_dict['base_name']
        self.id = id
        self.vae_name = vae_name
        self.path = path
        self.base_name = base_name

    def __str__(self):
        return "id: %s, vae_name: %s, path: %s, base_name: %s" % (self.id, self.vae_name, self.path, self.base_name)


    def to_dict(self):
        return {
            "id": self.id,
            "vae_name": self.vae_name,
            "path": self.path,
            "base_name": self.base_name
        }
        
