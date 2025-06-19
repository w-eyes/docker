# Заготовка для контейнера для Ubuntu18, cuda и ROS1


## Подготовка к соборке контейнера

1. Установить драйвера NVIDIA под свою карту
```
apt install nvidia-driver-570
```
2. Установить NVIDIA Container Tools

 [Официальная документация](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

```
# Добавляем репозиторий
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Обновляем данные репозиториев
sudo apt-get update

# Устанавливаем одинаковую версию (последняя на момент написания документации)
export NVIDIA_CONTAINER_TOOLKIT_VERSION=1.17.8-1
  sudo apt-get install -y \
      nvidia-container-toolkit=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      nvidia-container-toolkit-base=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      libnvidia-container-tools=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
      libnvidia-container1=${NVIDIA_CONTAINER_TOOLKIT_VERSION}


```


