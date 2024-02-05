import Frp_api
frp = Frp_api.frp_controller()

message_data = {
    'name' : 'frp_return', # 名称 mcsm_sw
    'request_type' : 'return_data', # 请求类型 task(任务) check(查看) return_data(返回数据)
    # 任务详情 data(任务数据)
    'data' : [{
    'switch' : 'off' # 开关 on开启 off关闭
    }], 
}

# 查看状态
if frp.state() == 'on':
    message_data['data'][0]['switch'] = 'on'
elif frp.state() == 'off':
    message_data['data'][0]['switch'] = 'off'


print(message_data)