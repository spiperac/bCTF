from apps.scoreboard.models import Configuration


def get_key(key):
    conf = Configuration.objects.filter(key=key).first()
    if conf:
        return conf.value
    else:
        return None
        
def set_key(key, value):
    conf = Configuration.objects.get(key=key)
    conf.value = value
    conf.save()

def create_key(key, value):
    Configuration.objects.create(
        key=key,
        value=value
    )