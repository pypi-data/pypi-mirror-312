# WS63自动下载脚本

## 安装流程

1. clone 本仓库
```shell
git clone https://github.com/geekheart/burntool.git
```

2. 安装本仓库的 python 包
```shell
cd burntool
pip install .
```

## 使用教程

1. burn --help
```shell
Usage: burn [OPTIONS] FIRMWARE_FILE

  烧录ws63固件

Options:
  -v, --verbose           打印一些调试信息.
  -p, --port TEXT         指定串口号.
  -b, --baudrate INTEGER  设置串口波特率.
  -s, --show              仅展示固件信息.
  --help                  Show this message and exit.
```

2. 烧录固件 

```shell
# linux
burn XXXXX.fwpkg -p /dev/ttyUSBx
# windows
burn XXXXX.fwpkg -p COMx
```

3. 仅展示固件信息
```shell
burn XXXXX.fwpkg -s
```

## 参考资料

[https://github.com/goodspeed34/ws63flash](https://github.com/goodspeed34/ws63flash)