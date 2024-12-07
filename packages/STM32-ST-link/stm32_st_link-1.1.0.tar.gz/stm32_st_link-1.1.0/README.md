# STM32_ST-link

`STM32_ST-link` 是基于 `STM32 ST-LINK Utility` 的一个命令行工具的封装，用于在命令行下对STM32芯片进行烧录、擦除、复位、验证等操作。
可用于无界面批量自动化烧录、测试
## 环境
 win10+python3.8

```bash
pip install STM32_ST-link
```
## 使用
```python
from STM32_ST_link import STLinkCLI

# 创建STLinkCLI实例
stlink = STLinkCLI()
# 连接到设备
if stlink.connect():    # ST-link 连接单片机
    stlink.erase()    # 擦除整个芯片（可选）

    # 烧录程序
    if stlink.program(
            file_path=r"bin/at803v1r1_baseband.bin",    # 烧录的固件文件
            address="0x08020000",   # 烧录地址
            verify=True,    # 烧录完验证
            reset=True      # 烧录完成复位
    ):
        print("Programming successful!")    # 烧录成功
```
