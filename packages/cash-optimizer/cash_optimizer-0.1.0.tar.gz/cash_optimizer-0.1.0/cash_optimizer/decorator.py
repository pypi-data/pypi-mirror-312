def cash_opt(func):
    def wrapper(*args, **kwargs):
        print(f"Executing function: {func.__name__}")
        print(f"Arguments: {args} {kwargs}")        
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} executed successfully.")
        return result

    return wrapper
