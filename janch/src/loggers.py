

async def cli(item, results):

    print(str({
        'item': item,
        **results
    }))


async def cli2(item, results):

    expecteds=[]
    actuals=[]
    matches=[]
    others=[]

    for k,v in results.items():
        expecteds.append({k:v['expected']})
        actuals.append({k:v['actual']})
        matches.append({k:v['match']})
        others.append({k:v['other']})

    print(f"{item}|{expecteds}|{actuals}|{matches}|{others}")


def get_default_loggers():
    return {
        'cli': {
            'method': cli
        }
    }
