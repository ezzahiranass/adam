import json




def iprint(title="", content=None):
    """
    print in an indented block
    """
    print(f"\n{title}")
    try:
        json_str = json.dumps(content, indent=4)
        print(json_str)
    except:
        print(content)
