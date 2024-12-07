import unittest
from unittest.mock import patch, MagicMock
from opsys_tec_controller.tec_controller import TecController


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(TecController, 'connect')
    def test_connect(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.connect()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'load_lut')
    def test_load_lut(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.load_lut()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'disconnect')
    def test_disconnect(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.disconnect()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'device_on')
    def test_device_on(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.device_on()
        tec_mock.assert_called_once_with()

    @ patch.object(TecController, 'device_off')
    def test_device_off(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.device_off()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'device_reset')
    def test_device_reset(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.device_reset()
        tec_mock.assert_called_once_with()

    @ patch.object(TecController, 'set_temperature')
    def test_set_temperature(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        temperature = 25
        tec_conn.set_temperature(temperature=temperature)
        tec_mock.assert_called_once_with(temperature=25)
        
    @ patch.object(TecController, 'get_temperature')
    def test_get_temperature(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_temperature()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'scan_temperature')
    def test_scan_temperature(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        scan_time = 5
        tec_conn.scan_temperature(scan_time=scan_time)
        tec_mock.assert_called_once_with(scan_time=5)
    
    @ patch.object(TecController, 'is_on')
    def test_is_on(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.is_on()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_system_error')
    def test_get_system_error(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_system_error()
        tec_mock.assert_called_once_with()
    
    @ patch.object(TecController, 'get_device_id')
    def test_get_device_id(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_device_id()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'reset_device_configs')
    def test_reset_device_configs(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.reset_device_configs()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_current_lower_limit')
    def test_get_current_lower_limit(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_current_lower_limit()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_current_higher_limit')
    def get_current_higher_limit(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_current_higher_limit()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_sensor_lower_protection')
    def get_sensor_lower_protection(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_sensor_lower_protection()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_sensor_higher_protection')
    def test_get_sensor_higher_protection(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_sensor_higher_protection()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_sensor_lower_temperature')
    def test_get_sensor_lower_temperature(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_sensor_lower_temperature()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_sensor_higher_temperature')
    def test_get_sensor_higher_temperature(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_sensor_higher_temperature()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'get_sensor_type')
    def test_get_sensor_type(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_sensor_type()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'set_sensor_type')
    def test_set_sensor_type(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        sensor_type = 'ICV'
        tec_conn.set_sensor_type(sensor_type=sensor_type)
        tec_mock.assert_called_once_with(sensor_type='ICV')
        
    @ patch.object(TecController, 'set_current_lower_limit')
    def test_set_current_lower_limit(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        limit = 1
        tec_conn.set_current_lower_limit(limit=limit)
        tec_mock.assert_called_once_with(limit=1)
        
    @ patch.object(TecController, 'set_current_higher_limit')
    def test_set_current_higher_limit(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        limit = 1
        tec_conn.set_current_higher_limit(limit=limit)
        tec_mock.assert_called_once_with(limit=1)
        
    @ patch.object(TecController, 'set_sensor_lower_protection')
    def test_set_sensor_lower_protection(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        limit = 1
        tec_conn.set_sensor_lower_protection(limit=limit)
        tec_mock.assert_called_once_with(limit=1)
    
    @ patch.object(TecController, 'set_sensor_higher_protection')
    def test_set_sensor_higher_protection(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        limit = 1
        tec_conn.set_sensor_higher_protection(limit=limit)
        tec_mock.assert_called_once_with(limit=1)
    
    @ patch.object(TecController, 'set_sensor_lower_temperature')
    def test_set_sensor_lower_temperature(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        limit = -40
        tec_conn.set_sensor_lower_temperature(limit=limit)
        tec_mock.assert_called_once_with(limit=-40)
        
    @ patch.object(TecController, 'set_sensor_higher_temperature')
    def test_set_sensor_higher_temperature(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        limit = 120
        tec_conn.set_sensor_higher_temperature(limit=limit)
        tec_mock.assert_called_once_with(limit=120)
        
    @ patch.object(TecController, 'get_sensor_value')
    def test_get_sensor_value(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_sensor_value()
        tec_mock.assert_called_once_with()
    
    @ patch.object(TecController, 'get_resistance')
    def test_get_resistance(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        tec_conn.get_resistance()
        tec_mock.assert_called_once_with()
        
    @ patch.object(TecController, 'set_resistance')
    def test_set_resistance(self, tec_mock: MagicMock):
        tec_conn = TecController(device_address='GPIB0::1::INSTR')
        resistance = 9.6
        tec_conn.set_resistance(resistance=resistance)
        tec_mock.assert_called_once_with(resistance=9.6)

    
if __name__ == '__main__':
    unittest.main()
