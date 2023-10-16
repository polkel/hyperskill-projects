def tagged(func):
    def wrapper(inp):
        new_inp = f"<title>{func(inp)}</title>"
        return new_inp

    return wrapper
