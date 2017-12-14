
def update_type_counter_aws_resource_record_set(type_counter_aws_resource_record_set: dict, record_type: str) -> dict:
    value = type_counter_aws_resource_record_set.get(record_type)
    if value is not None:
        type_counter_aws_resource_record_set[record_type] = value + 1
    else:
        type_counter_aws_resource_record_set[record_type] = 1
    return type_counter_aws_resource_record_set
