import unittest
from unittest.mock import patch, MagicMock
from opsys_tec_controller.ldt_5910c_controller import Idt5910cController
import pandas as pd

class TestIdt5910cController(unittest.TestCase):

    @patch('pyvisa.ResourceManager')
    def setUp(self, MockResourceManager):
        self.mock_rm = MockResourceManager.return_value
        self.mock_device = MagicMock()
        self.mock_rm.open_resource.return_value = self.mock_device
        self.controller = Idt5910cController('GPIB::1', 'resistance_to_temperature.csv')

    @patch('pandas.read_csv')
    def test_load_lut(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            'Nom': [0, 1, 2, 3],
            'Temp': [0, 10, 20, 30]
        })
        self.controller.load_lut()
        self.assertIsNotNone(self.controller._resistance_to_temp_db)
        self.assertEqual(self.controller.nom_resistances, [1.0, 2.0, 3.0])
        self.assertEqual(self.controller.temps, [10.0, 20.0, 30.0])

    def test_connect(self):
        self.assertTrue(self.controller.connect())
        self.mock_rm.open_resource.assert_called_with('GPIB::1')

    def test_disconnect(self):
        self.controller.connect()
        self.controller.disconnect()
        self.mock_device.close.assert_called_once()

    def test_device_on(self):
        self.controller.connect()
        self.controller.device_on()
        self.mock_device.write.assert_called_with(':OUTPut 1')

    def test_device_off(self):
        self.controller.connect()
        self.controller.device_off()
        self.mock_device.write.assert_called_with(':OUTPut 0')

    def test_device_reset(self):
        self.controller.connect()
        self.controller.device_reset()
        self.mock_device.write.assert_any_call(':OUTPut 0')
        self.mock_device.write.assert_any_call(':OUTPut 1')

    @patch('numpy.interp')
    @patch.object(Idt5910cController, 'set_sensor_value')
    def test_set_temperature(self, mock_set_sensor_value, mock_interp):
        mock_interp.return_value = 1.0
        self.controller.connect()
        self.controller.set_temperature(25)
        mock_interp.assert_called_once_with(25, self.controller.temps, self.controller.nom_resistances)
        mock_set_sensor_value.assert_called_once_with(1000.0)

    @patch.object(Idt5910cController, 'get_sensor_value')
    @patch('numpy.interp')
    def test_get_temperature(self, mock_interp, mock_get_sensor_value):
        mock_get_sensor_value.return_value = 1000
        mock_interp.return_value = 25.0
        self.controller.connect()
        temperature = self.controller.get_temperature()
        self.assertEqual(temperature, 25.0)
        mock_get_sensor_value.assert_called_once()
        mock_interp.assert_called_once_with(1.0, self.controller.nom_resistances[::-1], self.controller.temps[::-1])

    def test_get_device_id(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'ID'
        device_id = self.controller.get_device_id()
        self.assertEqual(device_id, 'ID')

    def test_clear_status(self):
        self.controller.connect()
        self.controller.clear_status()
        self.mock_device.write.assert_called_with('*CLS')

    def test_set_standard_event_status_enable(self):
        self.controller.connect()
        self.controller.set_standard_event_status_enable(40)
        self.mock_device.write.assert_called_with('*ESE 40')

    def test_get_standard_event_status_enable(self):
        self.controller.connect()
        self.mock_device.read.return_value = '68'
        status_enable = self.controller.get_standard_event_status_enable()
        self.assertEqual(status_enable, '68')

    def test_get_standard_event_status_register(self):
        self.controller.connect()
        self.mock_device.read.return_value = '32'
        status_register = self.controller.get_standard_event_status_register()
        self.assertEqual(status_register, '32')

    def test_get_identification(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'ID'
        identification = self.controller.get_identification()
        self.assertEqual(identification, 'ID')

    def test_set_operation_complete(self):
        self.controller.connect()
        self.controller.set_operation_complete()
        self.mock_device.write.assert_called_with('*OPC')

    def test_get_operation_complete(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1'
        operation_complete = self.controller.get_operation_complete()
        self.assertEqual(operation_complete, '1')

    def test_set_power_on_status_clear(self):
        self.controller.connect()
        self.controller.set_power_on_status_clear(1)
        self.mock_device.write.assert_called_with('*PSC 1')

    def test_get_power_on_status_clear(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1'
        power_on_status_clear = self.controller.get_power_on_status_clear()
        self.assertEqual(power_on_status_clear, '1')

    def test_recall(self):
        self.controller.connect()
        self.controller.recall(0)
        self.mock_device.write.assert_called_with('*RCL 0')

    def test_reset(self):
        self.controller.connect()
        self.controller.reset()
        self.mock_device.write.assert_called_with('*RST')

    def test_save(self):
        self.controller.connect()
        self.controller.save(3)
        self.mock_device.write.assert_called_with('*SAV 3')

    def test_set_service_request_enable(self):
        self.controller.connect()
        self.controller.set_service_request_enable(16)
        self.mock_device.write.assert_called_with('*SRE 16')

    def test_get_service_request_enable(self):
        self.controller.connect()
        self.mock_device.read.return_value = '16'
        service_request_enable = self.controller.get_service_request_enable()
        self.assertEqual(service_request_enable, '16')

    @patch.object(Idt5910cController, '_query')
    def test_get_status_byte(self, mock_query):
        self.controller.connect()
        mock_query.return_value = '200'
        status_byte = self.controller.get_status_byte()
        self.assertEqual(status_byte, '200')

    def test_self_test(self):
        self.controller.connect()
        self.mock_device.read.return_value = '0'
        self_test = self.controller.self_test()
        self.assertEqual(self_test, '0')

    def test_wait_to_continue(self):
        self.controller.connect()
        self.controller.wait_to_continue()
        self.mock_device.write.assert_called_with('*WAI')

    def test_set_analog_input(self):
        self.controller.connect()
        self.controller.set_analog_input('ON')
        self.mock_device.write.assert_called_with(':ANAloginput ON')

    def test_get_analog_input(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'ON'
        analog_input = self.controller.get_analog_input()
        self.assertEqual(analog_input, 'ON')

    def test_set_cable_resistance(self):
        self.controller.connect()
        self.controller.set_cable_resistance(0.02)
        self.mock_device.write.assert_called_with(':CABLER 0.02')

    def test_get_cable_resistance(self):
        self.controller.connect()
        self.mock_device.read.return_value = '0.02'
        cable_resistance = self.controller.get_cable_resistance()
        self.assertEqual(cable_resistance, '0.02')

    def test_set_ici_constants(self):
        self.controller.connect()
        self.controller.set_ici_constants(1.0, 0.0)
        self.mock_device.write.assert_called_with(':CONST:ICI 1.0,0.0')

    def test_get_ici_constants(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1.0,0.0'
        ici_constants = self.controller.get_ici_constants()
        self.assertEqual(ici_constants, '1.0,0.0')

    def test_set_ici_slope(self):
        self.controller.connect()
        self.controller.set_ici_slope(1.0)
        self.mock_device.write.assert_called_with(':CONST:ICI:SLOPe 1.0')

    def test_get_ici_slope(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1.0'
        ici_slope = self.controller.get_ici_slope()
        self.assertEqual(ici_slope, '1.0')

    def test_set_ici_offset(self):
        self.controller.connect()
        self.controller.set_ici_offset(0.0)
        self.mock_device.write.assert_called_with(':CONST:ICI:OFFSet 0.0')

    def test_get_ici_offset(self):
        self.controller.connect()
        self.mock_device.read.return_value = '0.0'
        ici_offset = self.controller.get_ici_offset()
        self.assertEqual(ici_offset, '0.0')

    def test_set_icv_constants(self):
        self.controller.connect()
        self.controller.set_icv_constants(10.0, 0.0)
        self.mock_device.write.assert_called_with(':CONST:ICV 10.0,0.0')

    def test_get_icv_constants(self):
        self.controller.connect()
        self.mock_device.read.return_value = '10.0,0.0'
        icv_constants = self.controller.get_icv_constants()
        self.assertEqual(icv_constants, '10.0,0.0')

    def test_set_icv_slope(self):
        self.controller.connect()
        self.controller.set_icv_slope(10.0)
        self.mock_device.write.assert_called_with(':CONST:ICV:SLOPe 10.0')

    def test_get_icv_slope(self):
        self.controller.connect()
        self.mock_device.read.return_value = '10.0'
        icv_slope = self.controller.get_icv_slope()
        self.assertEqual(icv_slope, '10.0')

    def test_set_icv_offset(self):
        self.controller.connect()
        self.controller.set_icv_offset(0.0)
        self.mock_device.write.assert_called_with(':CONST:ICV:OFFSet 0.0')

    def test_get_icv_offset(self):
        self.controller.connect()
        self.mock_device.read.return_value = '0.0'
        icv_offset = self.controller.get_icv_offset()
        self.assertEqual(icv_offset, '0.0')

    def test_set_rtd_constants(self):
        self.controller.connect()
        self.controller.set_rtd_constants(3.908, -5.775, -4.183, 100.0)
        self.mock_device.write.assert_called_with(':CONST:RTD 3.908,-5.775,-4.183,100.0')

    def test_get_rtd_constants(self):
        self.controller.connect()
        self.mock_device.read.return_value = '3.908,-5.775,-4.183,100.0'
        rtd_constants = self.controller.get_rtd_constants()
        self.assertEqual(rtd_constants, '3.908,-5.775,-4.183,100.0')

    def test_set_thermistor_constants(self):
        self.controller.connect()
        self.controller.set_thermistor_constants(1.125, 2.347, 0.855)
        self.mock_device.write.assert_called_with(':CONST:THERMistor 1.125,2.347,0.855')

    def test_get_thermistor_constants(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1.125,2.347,0.855'
        thermistor_constants = self.controller.get_thermistor_constants()
        self.assertEqual(thermistor_constants, '1.125,2.347,0.855')

    def test_set_display(self):
        self.controller.connect()
        self.controller.set_display('ON')
        self.mock_device.write.assert_called_with(':DISPLay ON')

    def test_get_display(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'ON'
        display = self.controller.get_display()
        self.assertEqual(display, 'ON')

    def test_set_display_brightness(self):
        self.controller.connect()
        self.controller.set_display_brightness(5)
        self.mock_device.write.assert_called_with(':DISPLay:BRIGHTness 5')

    def test_get_display_brightness(self):
        self.controller.connect()
        self.mock_device.read.return_value = '5'
        display_brightness = self.controller.get_display_brightness()
        self.assertEqual(display_brightness, '5')

    def test_set_enable_condition(self):
        self.controller.connect()
        self.controller.set_enable_condition(1)
        self.mock_device.write.assert_called_with(':ENABle:COND 1')

    def test_get_enable_condition(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1'
        enable_condition = self.controller.get_enable_condition()
        self.assertEqual(enable_condition, '1')

    def test_set_enable_event(self):
        self.controller.connect()
        self.controller.set_enable_event(1)
        self.mock_device.write.assert_called_with(':ENABle:EVEnt 1')

    def test_get_enable_event(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1'
        enable_event = self.controller.get_enable_event()
        self.assertEqual(enable_event, '1')

    def test_set_enable_output_off(self):
        self.controller.connect()
        self.controller.set_enable_output_off(1)
        self.mock_device.write.assert_called_with(':ENABle:OUTOFF 1')

    def test_get_enable_output_off(self):
        self.controller.connect()
        self.mock_device.read.return_value = '1'
        enable_output_off = self.controller.get_enable_output_off()
        self.assertEqual(enable_output_off, '1')

    def test_get_errors(self):
        self.controller.connect()
        self.mock_device.read.return_value = '0'
        errors = self.controller.get_errors()
        self.assertEqual(errors, '0')

    def test_get_event(self):
        self.controller.connect()
        self.mock_device.read.return_value = '2048'
        event = self.controller.get_event()
        self.assertEqual(event, '2048')

    def test_set_fan(self):
        self.controller.connect()
        self.controller.set_fan('ON')
        self.mock_device.write.assert_called_with(':FAN ON')

    def test_get_fan(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'ON'
        fan = self.controller.get_fan()
        self.assertEqual(fan, 'ON')

    def test_set_fan_voltage(self):
        self.controller.connect()
        self.controller.set_fan_voltage(12.0)
        self.mock_device.write.assert_called_with(':FAN:VOLTage 12.0')

    def test_get_fan_voltage(self):
        self.controller.connect()
        self.mock_device.read.return_value = '12.0'
        fan_voltage = self.controller.get_fan_voltage()
        self.assertEqual(fan_voltage, '12.0')

    def test_set_ite_high_limit(self):
        self.controller.connect()
        self.controller.set_ite_high_limit(2.5)
        self.mock_device.write.assert_called_with(':LIMit:ITE:HIgh 2.5')

    def test_get_ite_high_limit(self):
        self.controller.connect()
        self.mock_device.read.return_value = '2.5'
        ite_high_limit = self.controller.get_ite_high_limit()
        self.assertEqual(ite_high_limit, '2.5')

    def test_set_ite_low_limit(self):
        self.controller.connect()
        self.controller.set_ite_low_limit(-2.5)
        self.mock_device.write.assert_called_with(':LIMit:ITE:LOw -2.5')

    def test_get_ite_low_limit(self):
        self.controller.connect()
        self.mock_device.read.return_value = '-2.5'
        ite_low_limit = self.controller.get_ite_low_limit()
        self.assertEqual(ite_low_limit, '-2.5')

    def test_set_sensor_high_limit(self):
        self.controller.connect()
        self.controller.set_sensor_high_limit(4501.0)
        self.mock_device.write.assert_called_with(':LIMit:SENsor:HIgh 4501.0')

    def test_get_sensor_high_limit(self):
        self.controller.connect()
        self.mock_device.read.return_value = '4501.0'
        sensor_high_limit = self.controller.get_sensor_high_limit()
        self.assertEqual(sensor_high_limit, '4501.0')

    def test_set_sensor_low_limit(self):
        self.controller.connect()
        self.controller.set_sensor_low_limit(450.0)
        self.mock_device.write.assert_called_with(':LIMit:SENsor:LOw 450.0')

    def test_get_sensor_low_limit(self):
        self.controller.connect()
        self.mock_device.read.return_value = '450.0'
        sensor_low_limit = self.controller.get_sensor_low_limit()
        self.assertEqual(sensor_low_limit, '450.0')

    def test_set_temp_high_limit(self):
        self.controller.connect()
        self.controller.set_temp_high_limit(105.0)
        self.mock_device.write.assert_called_with(':LIMit:Temp:HIgh 105.0')

    def test_get_temp_high_limit(self):
        self.controller.connect()
        self.mock_device.read.return_value = '105.0'
        temp_high_limit = self.controller.get_temp_high_limit()
        self.assertEqual(temp_high_limit, '105.0')

    def test_set_temp_low_limit(self):
        self.controller.connect()
        self.controller.set_temp_low_limit(-20.0)
        self.mock_device.write.assert_called_with(':LIMit:Temp:LOw -20.0')

    def test_get_temp_low_limit(self):
        self.controller.connect()
        self.mock_device.read.return_value = '-20.0'
        temp_low_limit = self.controller.get_temp_low_limit()
        self.assertEqual(temp_low_limit, '-20.0')

    def test_set_tolerance(self):
        self.controller.connect()
        self.controller.set_tolerance(0.3)
        self.mock_device.write.assert_called_with(':LIMit:TOLerance 0.3')

    def test_get_measured_ite(self):
        self.controller.connect()
        self.mock_device.read.return_value = '2.2'
        measured_ite = self.controller.get_measured_ite()
        self.assertEqual(measured_ite, '2.2')

    def test_get_measured_sensor(self):
        self.controller.connect()
        self.mock_device.read.return_value = '0.0001323'
        measured_sensor = self.controller.get_measured_sensor()
        self.assertEqual(measured_sensor, '0.0001323')

    def test_get_measured_temp(self):
        self.controller.connect()
        self.mock_device.read.return_value = '45.6'
        measured_temp = self.controller.get_measured_temp()
        self.assertEqual(measured_temp, '45.6')

    def test_get_measured_vte(self):
        self.controller.connect()
        self.mock_device.read.return_value = '4.2'
        measured_vte = self.controller.get_measured_vte()
        self.assertEqual(measured_vte, '4.2')

    def test_set_mode(self):
        self.controller.connect()
        self.controller.set_mode('T')
        self.mock_device.write.assert_called_with(':MODE T')

    def test_get_mode(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'T'
        mode = self.controller.get_mode()
        self.assertEqual(mode, 'T')

    def test_set_output_on(self):
        self.controller.connect()
        self.controller.set_output('ON')
        self.mock_device.write.assert_called_with(':OUTPut ON')

    def test_set_output_off(self):
        self.controller.connect()
        self.controller.set_output('OFF')
        self.mock_device.write.assert_called_with(':OUTPut OFF')

    def test_get_output(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'ON'
        output = self.controller.get_output()
        self.assertEqual(output, 'ON')

    def test_set_pid(self):
        self.controller.connect()
        self.controller.set_pid(24.0, 5.6, 8.0)
        self.mock_device.write.assert_called_with(':PID 24.0,5.6,8.0')

    def test_get_pid(self):
        self.controller.connect()
        self.mock_device.read.return_value = '24.0,5.6,8.0'
        pid = self.controller.get_pid()
        self.assertEqual(pid, '24.0,5.6,8.0')

    def test_set_pid_autotune(self):
        self.controller.connect()
        self.controller.set_pid_autotune('RUN')
        self.mock_device.write.assert_called_with(':PID:ATUNE RUN')

    def test_get_pid_autotune(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'RUNNING'
        pid_autotune = self.controller.get_pid_autotune()
        self.assertEqual(pid_autotune, 'RUNNING')

    def test_set_pid_preset(self):
        self.controller.connect()
        self.controller.set_pid_preset('LDM4405')
        self.mock_device.write.assert_called_with(':PID:PRESET LDM4405')

    def test_get_pid_preset(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'LDM4405'
        pid_preset = self.controller.get_pid_preset()
        self.assertEqual(pid_preset, 'LDM4405')

    def test_set_radix(self):
        self.controller.connect()
        self.controller.set_radix('DECimal')
        self.mock_device.write.assert_called_with(':RADIX DECimal')

    def test_get_radix(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'DECimal'
        radix = self.controller.get_radix()
        self.assertEqual(radix, 'DECimal')

    def test_set_sensor(self):
        self.controller.connect()
        self.controller.set_sensor('THERM100UA')
        self.mock_device.write.assert_called_with(':SENsor THERM100UA')

    def test_get_sensor(self):
        self.controller.connect()
        self.mock_device.read.return_value = 'THERM100UA'
        sensor = self.controller.get_sensor()
        self.assertEqual(sensor, 'THERM100UA')

    def test_set_ite(self):
        self.controller.connect()
        self.controller.set_ite(2.5)
        self.mock_device.write.assert_called_with(':SET:ITE 2.5')

    def test_get_ite(self):
        self.controller.connect()
        self.mock_device.read.return_value = '2.5'
        ite = self.controller.get_ite()
        self.assertEqual(ite, '2.5')

    def test_set_sensor_value(self):
        self.controller.connect()
        self.controller.set_sensor_value(0.002932)
        self.mock_device.write.assert_called_with(':SET:SENsor 0.002932')

    def test_get_sensor_value(self):
        self.controller.connect()
        self.mock_device.read.return_value = '0.002932'
        sensor_value = self.controller.get_sensor_value()
        self.assertEqual(sensor_value, '0.002932')

    def test_set_temp(self):
        self.controller.connect()
        self.controller.set_temp(75.43)
        self.mock_device.write.assert_called_with(':SET:Temp 75.43')

    def test_get_temp(self):
        self.controller.connect()
        self.mock_device.read.return_value = '75.43'
        temp = self.controller.get_temp()
        self.assertEqual(temp, '75.43')
        
    @patch.object(Idt5910cController, '_query')
    def test_get_condition_status(self, mock_query):
        mock_query.return_value = '1'
        condition_status = self.controller.get_condition_status()
        mock_query.assert_called_once_with(":COND?")
        self.assertEqual(condition_status, '1')

    @patch.object(Idt5910cController, '_query')
    def test_get_status(self, mock_query):
        mock_query.return_value = 0x600
        status = self.controller.get_status()
        mock_query.assert_called_once_with(":STATus?")
        self.assertEqual(status, 0x600)

    @patch.object(Idt5910cController, '_send_command')
    def test_set_syntax(self, mock_send_command):
        self.controller.set_syntax(0)
        mock_send_command.assert_called_once_with(":SYNTAX 0")

        self.controller.set_syntax(1)
        mock_send_command.assert_called_with(":SYNTAX 1")
    
    @patch.object(Idt5910cController, '_query')
    def test_get_syntax(self, mock_query):
        mock_query.return_value = 0
        syntax = self.controller.get_syntax()
        mock_query.assert_called_once_with(":SYNTAX?")
        self.assertEqual(syntax, 0)
        
if __name__ == '__main__':
    unittest.main()