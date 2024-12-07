from .tec_abstract import TecAbstract
from .ldt_5910c_controller import Idt5910cController
from .device_types import DeviceTypes


class TecController(TecAbstract):
    """
    Thermoelectric Temperature Controller interface
    """

    def __init__(self,
                 device_type=DeviceTypes.Idt5910c,
                 device_address="",
                 lut_filepath=""):
        """
        constructor

        Args:
            device_type (str, optional): Device model name. Defaults to 'IDT-5910C'.
            device_address (str, optional): Device address. Defaults to ''.
            lut_filepath (str, optional): Resistance to Tempearture LUT file path. Defaults to ''.
        """
        self._device_type = device_type
        self._device_address = device_address
        self._lut_filepath = lut_filepath
        self._tec = None
        
    def load_lut(self, lut_filepath=None):
        """
        Load temperature to resistance LUT

        Args:
            lut_filepath (str, optiona): Resistance to temperature LUT path.
                                         Defaults to None.
        """
        self._tec.load_lut(lut_filepath)
    
    def connect(self):
        """
        connect to device
        
        Returns:
            bool: connection status.
                  True if conncted, else False.
        """
        if self._device_type == DeviceTypes.Idt5910c:
            self._tec = Idt5910cController(self._device_address, self._lut_filepath)
        else:
            raise ValueError("Can't find device type")
        
        return self._tec.connect()
            
    def disconnect(self):
        """
        Disconnect from device
        """
        self._tec.disconnect()
        print('Tec disconnected!')

    def device_on(self):
        """
        Set power on
        """
        self._tec.device_on()
        print('Tec power on!')

    def device_off(self):
        """
        Set power off
        """
        self._tec.device_off()
        print('Tec power off!')
        
    def device_reset(self):
        """
        Reset TEC
        """
        self._tec.device_reset()
        print('Reset Tec succeeded!')
    
    def set_temperature(self, temperature):
        """
        Set temperature value

        Args:
            temperature (int): Temperature setpoint.
        """
        self._tec.set_temperature(temperature)
        print(f'Set temperature to: {temperature}')
    
    def get_temperature(self):
        """
        Get current temperature value
        
        Returns:
            float: temperature
        """
        return self._tec.get_temperature()

    def scan_temperature(self, scan_time):
        """
        Scan temperature value
        
        Args:
            scan_time (float): Scanning time in sec.
        
        Returns:
            list: temperature samples list
        """
        print(f'Temperature scanning started: {scan_time} sec')
        return self._tec.scan_temperature(scan_time)

    def is_on(self):
        """
        Checking if the device is on (output voltage exists)

        Returns:
            bool: On/Off status
        """
        return self._tec.is_on()

    def get_system_error(self):
        """
        Get system errors

        Returns:
            str: system errors info
        """
        return self._tec.get_system_error()

    def get_device_id(self):
        """
        Read device id
        
        Returns:
            bool: device ID string
        """
        return self._tec.get_device_id()

    def reset_device_configs(self):
        """
        Reset device configurations
        """
        self._tec.reset_device_configs()
        print('Reset Device configurations succeeded!')
        
    def get_current_lower_limit(self):
        """
        Get current lower limit

        Returns:
            float: min current value (A)
        """
        limit = self._tec.get_current_lower_limit()
        return limit

    def set_current_lower_limit(self, limit):
        """
        Set current lower limit

        Args:
            limit (float): min current value (A)
        """
        self._tec.set_current_lower_limit(limit)
        print(f'Current lower protection limit set to: {limit}')
        
    def get_current_higher_limit(self):
        """
        Get current higher limit

        Returns:
            float: max current value (A)
        """
        limit = self._tec.get_current_higher_limit()
        return limit

    def set_current_higher_limit(self, limit):
        """
        Set current higher limit

        Args:
            limit (float): max current value (A)
        """
        self._tec.set_current_higher_limit(limit)
        print(f'Current higher protection limit set to: {limit}')
        
    def get_sensor_lower_protection(self):
        """
        Get sensor lower protection limit

        Returns:
            float: lower limit (resistance|µA|mV)
        """
        limit = self._tec.get_sensor_lower_protection()
        return limit

    def set_sensor_lower_protection(self, limit):
        """
        Set sensor lower protection limit

        Args:
            limit (float): lower limit (resistance|µA|mV)
        """
        self._tec.set_sensor_lower_protection(limit)
        print(f'Sensor lower protection limit set to: {limit}')
        
    def get_sensor_higher_protection(self):
        """
        Get sensor higher protection limit

        Returns:
            float: higher limit (resistance|µA|mV)
        """
        limit = self._tec.get_sensor_higher_protection()
        return limit

    def set_sensor_higher_protection(self, limit):
        """
        Set sensor higher protection limit

        Args:
            limit (float): higher limit (resistance|µA|mV)
        """
        self._tec.set_sensor_higher_protection(limit)
        print(f'Sensor higher protection limit set to: {limit}')
        
    def get_sensor_lower_temperature(self):
        """
        Get sensor lower temperature limit

        Returns:
            float: lower limit (degrees)
        """
        limit = self._tec.get_sensor_lower_temperature()
        return limit
        
    def set_sensor_lower_temperature(self, limit):
        """
        Set sensor lower temperature limit

        Args:
            limit (float): lower limit (degrees)
        """
        self._tec.set_sensor_lower_temperature(limit)
        print(f'Sensor lower temperature limit set to: {limit}')
        
    def get_sensor_higher_temperature(self):
        """
        Get sensor higher temperature limit

        Returns:
            float: lower limit (degrees)
        """
        limit = self._tec.get_sensor_higher_temperature()
        return limit

    def set_sensor_higher_temperature(self, limit):
        """
        Set sensor higher temperature limit

        Args:
            limit (float): higher limit (degrees)
        """
        self._tec.set_sensor_higher_temperature(limit)
        print(f'Sensor higher temperature limit set to: {limit}')
        
    def get_sensor_type(self):
        """
        Get selected sensor type (ICI|ICV...)
        
        Returns:
            str: sensor type
        """
        return self._tec.get_sensor_type()
    
    def set_sensor_type(self, sensor_type):
        """
        Set sensor type (ICI|ICV...)
        
        Args:
            sensor_type (str): sensor type
        """
        self._tec.set_sensor_type(sensor_type)
        print(f'Sensor type set: {sensor_type}')

    def get_sensor_value(self):
        """
        Get selected sensor measured value (R, A, mV)
        
        Retruns:
            float: measured value
        """
        return self._tec.get_sensor_value()
    
    def get_resistance(self):
        """
        Get output cable resistance
        
        Retruns:
            float: cable resistance (ohm)
        """
        return self._tec.get_resistance()
    
    def set_resistance(self, resistance):
        """
        Get output cable resistance
        
        Args:
            resistance (float): resistance value
        """
        self._tec.set_resistance(resistance)
        print(f'Resistance set to: {resistance}')
