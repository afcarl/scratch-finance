from jsonbin import utils

equities = utils.initialize(path='common/equities.csv')
equities = utils.populate(equities)
json = utils.create_json(equities)
if len(json) > 0:
    print(utils.put_json(json))
