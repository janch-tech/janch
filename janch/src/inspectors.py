
async def equals(gathered, settings):
    return gathered == settings



def get_default_inspectors():
    return {
        'equals': equals
    }
