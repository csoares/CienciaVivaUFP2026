

# Testar SLAM no JetRacer com ROS Melodic + RPLIDAR + Foxglove

## Objetivo

Visualizar em tempo real:

- Dados do RPLIDAR (`/scan`)
- Transformações TF (`/tf`)
- Mapa SLAM (`/map`)
- Posição do robô (`/odom`)
- Outros tópicos ROS

utilizando o Foxglove Studio ligado ao JetRacer.

---

# 1. Arrancar o ROS Master

Terminal 1:

```bash
source /opt/ros/melodic/setup.bash
roscore
```

Verificar:

```bash
rosnode list
```

Deve aparecer:

```text
/rosout
```

---

# 2. Arrancar o RPLIDAR

Terminal 2:

```bash
source /opt/ros/melodic/setup.bash
roslaunch jetracer lidar.launch
```

Verificar:

```bash
rostopic list
```

Deve existir:

```text
/scan
```

Testar:

```bash
rostopic hz /scan
```

Resultado esperado:

```text
average rate: ~10 Hz
```

---

# 3. Arrancar o SLAM

## Opção A - Hector SLAM

Terminal 3:

```bash
source /opt/ros/melodic/setup.bash
roslaunch hector_slam_launch tutorial.launch
```

ou

```bash
source /opt/ros/melodic/setup.bash
roslaunch hector_mapping mapping_default.launch
```

Verificar:

```bash
rostopic list
```

Devem aparecer:

```text
/map
/map_metadata
/poseupdate
/slam_out_pose
```

---

## Opção B - GMapping

Terminal 3:

```bash
source /opt/ros/melodic/setup.bash
roslaunch gmapping slam_gmapping.launch
```

Verificar:

```bash
rostopic list
```

Devem aparecer:

```text
/map
/map_metadata
```

---

# 4. Instalar Foxglove Bridge

(Testado - funciona bem)

O ROS Master tem de estar ativo.

```bash
sudo apt update
sudo apt install ros-melodic-foxglove-bridge
```

---

# 5. Arrancar Foxglove Bridge

Terminal 4:

```bash
source /opt/ros/melodic/setup.bash
roslaunch --screen foxglove_bridge foxglove_bridge.launch port:=8765
```

Verificar:

```text
WebSocket server listening on port 8765
```

---

# 6. Obter IP da Jetson

```bash
hostname -I
```

Exemplo:

```text
192.168.1.83
```

---

# 7. Ligar Foxglove Studio

No Foxglove Studio:

**Open Connection → Foxglove WebSocket**

URL:

```text
ws://192.168.1.83:8765
```

Substituir pelo IP real da Jetson.

---

# 8. Visualizações recomendadas no Foxglove

## LaserScan

Adicionar painel:

```text
Raw Messages
```

ou

```text
3D Panel
```

Selecionar:

```text
/scan
```

---

## TF

Adicionar:

```text
3D Panel
```

Selecionar:

```text
/tf
```

---

## Mapa SLAM

Adicionar:

```text
Map
```

Selecionar:

```text
/map
```

---

## Pose do robô

Selecionar:

```text
/slam_out_pose
```

ou

```text
/odom
```

consoante o algoritmo SLAM utilizado.

---

# 9. Verificação rápida

Verificar nós ativos:

```bash
rosnode list
```

Exemplo:

```text
/rplidarNode
/hector_mapping
/foxglove_bridge
/rosout
```

---

Verificar tópicos:

```bash
rostopic list
```

Esperado:

```text
/scan
/map
/tf
/tf_static
/rosout
```

---

# 10. Guardar mapa (opcional)

Quando terminares o mapeamento:

```bash
rosrun map_server map_saver -f mapa_jetracer
```

Serão criados:

```text
mapa_jetracer.pgm
mapa_jetracer.yaml
```

---

# Sequência resumida

Terminal 1:

```bash
roscore
```

Terminal 2:

```bash
roslaunch jetracer lidar.launch
```

Terminal 3:

```bash
roslaunch hector_slam_launch tutorial.launch
```

Terminal 4:

```bash
roslaunch --screen foxglove_bridge foxglove_bridge.launch port:=8765
```

Foxglove:

```text
ws://<IP_DA_JETSON>:8765
```
````

Uma nota específica para o teu JetRacer: como não tens encoders de roda e já verificaste que o RPLIDAR funciona em `/dev/ttyACM1`, o **Hector SLAM** tende a funcionar melhor do que o GMapping para uma primeira experiência de SLAM, porque consegue mapear usando essencialmente apenas os dados do LiDAR.
