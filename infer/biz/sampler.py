from diffusers import DPMSolverMultistepScheduler


class SAMPLER():

    SAMPLER_MAP = {}
    
    def __init__(self, pipe):
        self.pipe = pipe
        self.init_sampler_map()
    
    def load(self, sampler_id):
        return self.SAMPLER_MAP.get(sampler_id, None)
    
    
    def init_sampler_map(self):
        self.SAMPLER_MAP['DPM++ 2M Karras'] = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config, algorithm_type="dpmsolver++", solver_order=2)    
    
    