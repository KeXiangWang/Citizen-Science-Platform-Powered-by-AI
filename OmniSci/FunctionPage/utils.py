def is_pc(agent):
    agent = agent.lower()
    keywords = ["mobile","android","iphone","ipad","phone"]
    for item in keywords:
        if item in agent:
            return False
    return True