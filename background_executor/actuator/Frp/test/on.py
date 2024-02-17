# import Frp_api
# frp = Frp_api.frp_controller()
# frp.switch('on')
import subprocess

subprocess.run("nohup sh /home/chen/termux-manager/background_executor/actuator/Frp/frpc/qi.sh > /home/chen/termux-manager/background_executor/actuator/Frp/frpc/nohup.out 2>&1 &", shell=True)

# nohup sh /home/chen/termux-manager/background_executor/actuator/Frp/frpc/qi.sh > /home/chen/termux-manager/background_executor/actuator/Frp/frpc/out.file 2>&1 &
