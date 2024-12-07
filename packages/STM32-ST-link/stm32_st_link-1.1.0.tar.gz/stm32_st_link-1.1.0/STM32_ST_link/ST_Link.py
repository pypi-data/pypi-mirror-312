#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/12 下午3:06
# @Author  : 周梦泽
# @File    : ST_Link.py
# @Software: PyCharm
# @Description:STM32_ST-Link-CLI单片机操作：连接、烧录、擦除，使用前必须安装STM32 ST-LINK Utility


import subprocess
import os
from typing import Optional, List, Tuple
import logging


class STLinkCLI:
    """
    ST-LINK CLI命令行工具的Python封装类
    """

    def __init__(self, logging_level: int = logging.INFO):
        """
        初始化ST-LINK CLI封装类

        Args:
            logging_level: 日志级别
        """

        current_dir = os.path.dirname(__file__)
        self.cli_path = os.path.join(current_dir, 'ST_Link_CLI/ST-LINK_CLI.exe')
        # print(current_dir)
        # print(self.cli_path)

        # 配置日志
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('STLinkCLI')

    def _execute_command(self, command: List[str]) -> Tuple[int, str, str]:
        """
        执行ST-LINK CLI命令

        Args:
            command: 完整的命令参数列表

        Returns:
            (返回码, 标准输出, 标准错误)的元组
        """
        try:
            self.logger.info(f"执行命令{command}")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'
            )

            stdout, stderr = process.communicate()
            return process.returncode, stdout, stderr
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            raise

    def connect(self, serial_number: Optional[str] = None) -> bool:
        """
        连接到ST-LINK设备

        Args:
            serial_number: ST-LINK设备序列号(可选)

        Returns:
            连接是否成功
        """
        command = [self.cli_path, "-c"]
        if serial_number:
            command.extend(["-SN", serial_number])

        returncode, stdout, stderr = self._execute_command(command)
        success = returncode == 0

        if success:
            self.logger.info("Successfully connected to ST-LINK device")
        else:
            self.logger.error(f"Failed to connect to ST-LINK device: {stderr}")

        return success

    def program(self,
                file_path: str,
                address: Optional[str] = None,
                verify: bool = True,
                reset: bool = True) -> bool:
        """
        编程操作

        Args:
            file_path: 要烧录的二进制文件路径
            address: 起始地址(可选)
            verify: 是否在编程后进行验证
            reset: 是否在编程后复位目标

        Returns:
            编程操作是否成功
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Program file not found: {file_path}")

        command = [self.cli_path, "-P", file_path]

        if address:
            command.extend([address])
        if verify:
            command.append("-V")
        if reset:
            command.append("-Rst")

        returncode, stdout, stderr = self._execute_command(command)
        success = returncode == 0

        if success:
            self.logger.info(f"Successfully programmed file: {file_path}")
            if stdout:
                self.logger.debug(f"Program output: {stdout}")
        else:
            self.logger.error(f"Programming failed. Return code: {returncode}")
            if stdout:
                self.logger.error(f"Program output: {stdout}")
            if stderr:
                self.logger.error(f"Program error: {stderr}")

        return success

    def verify(self, file_path: str, address: Optional[str] = None) -> bool:
        """
        验证操作

        Args:
            file_path: 要验证的二进制文件路径
            address: 起始地址(可选)

        Returns:
            验证是否成功
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Verify file not found: {file_path}")

        command = [self.cli_path, "-V", file_path]
        if address:
            command.extend(["-P", address])

        returncode, stdout, stderr = self._execute_command(command)
        success = returncode == 0

        if success:
            self.logger.info(f"Successfully verified file: {file_path}")
        else:
            self.logger.error(f"Verification failed: {stderr}")

        return success

    def erase(self, start_addr: Optional[str] = None, size: Optional[str] = None) -> bool:
        """
        擦除操作

        Args:
            start_addr: 起始地址(可选)
            size: 擦除大小(可选)

        Returns:
            擦除是否成功
        """
        command = [self.cli_path, "-ME"]

        if start_addr and size:
            command.extend(["-S", start_addr, size])
        returncode, stdout, stderr = self._execute_command(command)
        success = returncode == 0

        if success:
            self.logger.info("Successfully erased memory")
        else:
            self.logger.error(f"Erase operation failed: {stderr}")

        return success

    def reset(self) -> bool:
        """
        复位目标设备

        Returns:
            复位操作是否成功
        """
        command = [self.cli_path, "-Rst"]
        returncode, stdout, stderr = self._execute_command(command)
        success = returncode == 0

        if success:
            self.logger.info("Successfully reset target")
        else:
            self.logger.error(f"Reset operation failed: {stderr}")

        return success


if __name__ == '__main__':
    # 创建STLinkCLI实例
    stlink = STLinkCLI(logging_level=logging.DEBUG)

    # 连接到设备
    if stlink.connect():
        stlink.erase()    # 擦除整个芯片

        # 烧录程序
        if stlink.program(
                file_path=r"bin/at803v1r1_baseband.bin",
                address="0x08020000",
                verify=True,
                reset=True
        ):
            print("Programming successful!")
