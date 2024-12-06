def transform_to_snake_case(data):
    if isinstance(data, dict):
        return {
            (
                key.replace("-", "_") if isinstance(key, str) else key
            ): transform_to_snake_case(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [transform_to_snake_case(item) for item in data]
    else:
        return data
