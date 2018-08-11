def set_not_none_dict_kwargs(dictionary: dict, **kwargs):
    if dictionary and isinstance(dictionary, dict):
        for k, v in kwargs.items():
            if v is not None:
                dictionary[k] = v
