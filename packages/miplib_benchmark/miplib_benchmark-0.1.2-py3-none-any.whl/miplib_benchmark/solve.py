import highspy
from .instance import get_instance_path
from .logger import logger

def print_info(info):
    # Get all attributes that don't start with '_' (non-private attributes)
    for attr in dir(info):
        if not attr.startswith('_'):  # Skip private/magic methods
            value = getattr(info, attr)
            print(f"{attr}: {value}")

def solve(instance_name: str, time_limit: int = 20):
    instance_path = get_instance_path(instance_name)
    model = highspy.Highs()
    model.setOptionValue("time_limit", time_limit)
    model.readModel(str(instance_path))
    model.run()
    highs_info = model.getInfo()
    print_info(highs_info)
    model.clear() 
    return highs_info
