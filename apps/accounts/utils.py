

def generate_color(username):
    first_three = username[:3]
    last_three = username[-3:]
    hexed = "".join("{:02x}".format(ord(c)) for c in first_three)
    hexed = "".join("{:02x}".format(ord(c)) for c in last_three)
    return "#{0}".format(hexed)
