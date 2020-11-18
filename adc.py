import spidev
from Adafruit_GPIO import SPI
from mcp3208 import MCP3208

# number of channels to read from ADC,
# MCP3208: 8 channels
_MAX_CHANNELS = 8
_EXC_MSG = "MCP3208 channel must be 0-7: "


class MCP3208Adafruit(MCP3208):
    """
    using Adafruit_GPIO.SPI,
    Hardware-based SPI implementation using the spidev interface.
    """

    def __init__(self, device: int = 0, speed: int = 1_000_000):
        self.__port = 0
        self.__device = device
        self.__speed = speed
        super().__init__()
        self.__init_spi()

    def __init_spi(self):
        self.spi = SPI.SpiDev(self.__port, self.__device,
                              max_speed_hz=self.__speed)
        self.spi.set_mode(0)
        self.spi.set_bit_order(SPI.MSBFIRST)

    def read(self, channel):
        if _MAX_CHANNELS <= channel < 0:
            raise Exception(f"{_EXC_MSG}{channel}")
        return super(MCP3208Adafruit, self).read(channel)


class MCP3208Spidev:
    """
    using built-in module spidev
    """

    def __init__(self, device: int = 0, speed: int = 1_000_000):
        # noinspection LongLine
        """
        :param device: Raspberry chip set CE 0 - BCM8 (GPIO8) PIN24 or CE 1 - BCM7 (GPIO7) PIN26, 0 per default
        :param speed: Maximum speed in Hz, 1 MHz per default
        """

        self.__speed = speed
        self.__device = device
        self.__bus = 0
        self.__adc = 0
        self.__data = 0
        self.__spi = None
        self.__init_spi()

    def __del__(self):
        self.__spi.close()

    def __init_spi(self):
        self.__spi = spidev.SpiDev()
        self.__spi.open(self.__bus, self.__device)
        self.__spi.max_speed_hz = self.__speed

    def read(self, channel: int):
        """
        Read input channel of MCP3208
        https://www.vampire.de/index.php/2018/05/06/raspberry-pi-mit-mcp3208/
        :param channel: 0-7 (D0 - D7 of MCP3208)
        :return: raw data value (12bit 0 - 4095)
        """
        if _MAX_CHANNELS <= channel < 0:
            raise Exception(f"{_EXC_MSG}{channel}")

        self.__adc = self.__spi.xfer2(
            [
                6 | (channel & 4) >> 2,
                (channel & 3) << 6,
                0
            ])
        self.__data = ((self.__adc[1] & 15) << 8) + self.__adc[2]
        return self.__data


if __name__ == '__main__':
    pass
