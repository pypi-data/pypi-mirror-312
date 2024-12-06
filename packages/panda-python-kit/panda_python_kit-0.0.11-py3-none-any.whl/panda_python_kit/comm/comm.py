def get_param_str_from_param_map( param_dict):
    if not param_dict:
        return ""
    param_str_parts = ["%s=%s" % (k, v) for k, v in sorted(param_dict.items())]
    return "&".join(param_str_parts)

def get_request_data(request):
    """根据请求类型获取请求参数"""
    if request.method == 'GET':
        # 对于GET请求, 获取URL的查询参数
        return request.args
    elif request.method == 'POST':
        # 对于POST请求，预期请求体为JSON
        return request.get_json()
    else:
        # 可以扩展以支持其他HTTP方法
        return {}
