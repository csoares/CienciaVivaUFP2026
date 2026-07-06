
# Uso de foxglove

## Robot

sudo apt install ros-melodic-foxglove-bridge
roslaunch --screen foxglove_bridge foxglove_bridge.launch port:=8765

sugestão abrir terminal ao lado e confirmar com comandos ros:
rosnode list
rosnode info teleop_joy


## Do lado da Foxglove app
-Dashboard -> Open connection
-Abrir/escolher Foxglove WebSocket (eg url: ws://192.168.1.83:8765)
-Adicionar painel teleop
-Adicionar topico /cmd_vel