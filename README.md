# Контейнер с Ubuntu 18.04, Cuda и ROS1

## TO DO

- [ ] Сделать контейнер для Uuntu 20.04 и Melodic
- [ ] Сделать обёртку для сборки. (На самом деле взять готовую из и адаптировать под нас)



## Подготовка к соборке контейнера
Подразумевается, что у вас установлена Ubuntu 24 любым способом: Bare Metall, VPS, WSL. 

1. Установить драйвера NVIDIA под свою карту.
```
apt install nvidia-driver-570
```
Убедиться что команда `nvidia-smi` отрабатывает и показывает корректные данные.

Если используется WSL2, то убедитесь, что присутствует переменная окружения MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA

2. Установить Docker

Здесь можно пойти двумя путями и поставить docker.io из официальных репозиториев Ubuntu или сборкой от docker. Считается, что docker.io более стабилен. Будем ставить его: 

```
apt install docker.io docker-buildx docker-compose-v2
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

Внимание! Rootless mode мы не будем использовать, т.к он накладывает ограничения на использование контейнера. А т.к. мы запускаем полноценную ОС c графикой и пробрасываем сеть, то будем использовать именно группу docker. 

## Проверка, что карточка пробрасывается в docker

```
docker run -it --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu18.04 nvidia-smi
```

Вместо nvidia/cuda:11.0.3-base-ubuntu18.04 можно успользовать и другие образы. Смотреть таги [Тут](https://hub.docker.com/r/nvidia/cuda/tags)


## Сборка и запуск контейнера

```
# После клонирования репозитория

cd docker/ubuntu18

# Сборка производится из папки, где лежит dockerfile

docker buildx build -t ros-melodic-ml . 

# Запуск без графики. Карта используется для вычислений.

docker run -it \
  --name ros-melodic-ml \
  --rm \
  --gpus all \
  --volume=$HOME/docker/ubuntu18/ros_ws:/ros_ws \
  ros-melodic-ml \
  bash

# При выходе контейнер убивается, все сделанные изменения в контейнере теряются. Если ясно, что внутри контейнера нужны какие-то пакеты и библиотеки, то лучше вносить измененияв dockerfile, тестировать работоспосбность и пересобирать контейнер.
#Рабочая папка ros_ws пробрасывается на сервер, в ней можно проводить основные работы, сохранять файлы.

# В соседней консоли можно также зайти в уже запущеный контейнер, т.к. для ROS одного терминала мало.

docker exec -it ros-melodic-ml bash

```
## Как проверить, что Cuda работает

В папке ubuntu18/ros_ws/src/cuda_tests находятся скрипты для быстрой проверки вычислений на GPU. Скрипты на python запускаются через python3, например ```python3 cpu_gpu_test.py```, а nvcc_test.cu сначала надо скомпилировать с помощью команды ```nvcc test.cu -o test```

## Графика

Для проверки графики можно запускать glxgears, mate-terminal и т.д.

### WSL2

Убедитесь, что присутствует переменная окружения MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA

```
docker run -it \
  --name ros-melodic-ml \
  --rm \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
  -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
  --volume=/tmp/.X11-unix:/tmp/.X11-unix \
  --volume="/mnt/wslg:/mnt/wslg" \
  --volume=~/docker/ubuntu18/ros_ws:/ros_ws \
  ros-melodic-ml \
  bash

```
Из консоли можно запускать грфические приложения. Если нужно запустить полноценную графическую оболчку , то можно воспользоваться виртуальным X сервером Xephyr. В контейнере выполняем:

```
Xephyr :1 -screen 1200x800 -ac -br -noreset +extension RANDR +extension GLX &
DISPLAY=:1 mate-session
```
И получаем полноценную графическую оболчку.

### Ubuntu 24

Из-за WayLand в Ubuntu 24 может некорретно пробрасываться графика и нужно будет запускать сессию "Ubuntu on XOrg"

```
# Если GPU отсутствует, то надо убрать --gpus all

# Включаем графику для локального пользователя. Потенциально опасная настройка, рекомендуется после использования контейнера выполнить xhost -local:docker

xhost +local:docker 

docker run -it \
  --name ros-melodic-ml \
  --rm \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  ${XDG_RUNTIME_DIR:+-e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR} \
  ${WAYLAND_DISPLAY:+-e WAYLAND_DISPLAY=$WAYLAND_DISPLAY} \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ${XDG_RUNTIME_DIR:+-v $XDG_RUNTIME_DIR:$XDG_RUNTIME_DIR} \
  ${WSL_INTEROP:+-v /mnt/wslg:/mnt/wslg} \
  --volume="$HOME/docker/ubuntu18/ros_ws:/ros_ws" \
  ros-melodic-ml \
  bash
```

### Удалённый доступ к серверу

Основная идея заключается в запуске полноценного desktop окружения в контейнере с помощью XPRA и проброс портов на сервер, а от туда по ssh на локальный ПК. XPRA позволяет отключиться от экрана и подключиться вновь.

Для начала нужно положить личный ssh ключ в ./ssh/autorized_keys на сервер. Это можно сделать через меня, прислав мне public key.

После этого нужно подключиться к серверу с пробросом порта: 
```
ssh dockeruser@server -L 14500:127.0.0.1:14500
```
Запускаем контейнер следующей командой:
```
docker run -it \
  --name ros-melodic-ml \
  --rm \
  --gpus all \
  -v ~/docker/ubuntu18/ros_ws:/ros_ws \
  -p 127.0.0.1:14500:14500 \
  ros-melodic-ml \
  bash -c "/root/start-xpra.sh & tail -f /dev/null"
# Используйте & для запуска в фоне и docker stop ros-melodic-ml для остановки контейнера
```
Теперь на локальном компьютере открыт порт 14500. Мы можем подключиться с помощью xpra attach через консоль, выполнив на локальном компьютере ```xpra attach tcp://localhost:14500``` или настроив через графический интерфейс.

Если не хочется использовать всё окружение, то можно зайти в контейнер и запустить нужное приложение (в примере запустится mate-terminal) вручную:

```
# На сервере
docker run -it \
  --name ros-melodic-ml \
  --rm \
  --gpus all \
  -v ~/docker/ubuntu18/ros_ws:/ros_ws \
  -p 127.0.0.1:14500:14500 \
  ros-melodic-ml \
  bash

# Внутри контейнера

xpra start:100 \
  --bind-tcp=0.0.0.0:14500 \
  --html=on \
  --start-child="mate-terminal" \
  --resize-display=yes \
  --desktop-scaling=1920x1080 \
  --exit-with-children \
  --clipboard=yes \
  --notifications=no \
  --compress=9 \
  --bell=no \
  --quality=50 \
  --speed=50 \
  --encoding=jpeg \
  --daemon=no 
```
После этого также подключаемся ```xpra attach tcp://localhost:14500``` и видим отдельное окно терминала, запущенного в контейнере на сервере.
