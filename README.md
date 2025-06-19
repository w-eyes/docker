# Контейнер с Ubuntu18, cuda и ROS1

## TO DO

- [ ] Сделать контейнер для Uuntu 20 и Melodic
- [ ] Сделать обёртку для сборки. (На самом деле взять готовую из и адаптировать под нас)



## Подготовка к соборке контейнера

1. Установить драйвера NVIDIA под свою карту.
```
apt install nvidia-driver-570
```
Убедиться что команда `nvidia-smi` отрабатывает и показывает корректные данные.

2. Установить Docker

Здесь можно пойти двумя путями и поставить docker.io из официальных репозиториев Ubuntu или сборкой от docker. Считается, что docker.io более стабилен. Будем ставить его: 

```
apt install docker.io

```



3. Установить NVIDIA Container Tools

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

4. Настроаивем docker и Nvidia

```
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Для того, чтобы можно было пользоваться контейнерами от обычного пользователя, надо добавить себя в группу docker `sudo usermod -aG docker $USER` и перезайти. 

## Проверка, что карточка пробрасывается в docker

```
docker run -it --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu18.04 nvidia-smi
```

Вместо nvidia/cuda:11.0.3-base-ubuntu18.04 можно успользовать и другие образы. Смотреть таги [Тут](https://hub.docker.com/r/nvidia/cuda/tags)


## Сборка и запуск контейнера

```
# После клонирования репозитория

cd ubuntu18

# Сборка производится из папки, где лежит dockerfile

docker build -t ros-melodic-ml . 

#

docker run -it --name ros-melodic-ml --rm --gpus all -v ~/docker/ubuntu18/ros_ws:/ros_ws ros-melodic-ml bash

# При выходе контейнер убивается, все сделанные изменения в контейнере теряются. Если ясно, что внутри контейнера нужны какие-то пакеты и библиотеки, то лучше вносить измененияв dockerfile, тестировать работоспосбность и пересобирать контейнер.
#Рабочая папка ros_ws пробрасывается на сервер, в ней можно проводить основные работы, сохранять файлы.

# В соседней консоли можно также зайти в уже запущеный контейнер, т.к. для ROS одного терминала мало.

docker exec -it ros-melodic-ml bash

```
