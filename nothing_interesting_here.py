from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import csv

KILL_SHOW_MSG_THREAD = False

def get_temp(sense):
	return sense.get_temperature()

def get_press(sense):
	return sense.get_pressure()

def get_hum(sense):
	return sense.get_humidity()

def get_orientation(sense):
	sense_orient = []
	orientation = sense.get_orientation()

	sense_orient.append(orientation["yaw"])
	sense_orient.append(orientation["pitch"])
	sense_orient.append(orientation["roll"])
	return sense_orient

def get_mag(sense):
	sense_mag = []
	mag = sense.get_compass_raw()

	sense_mag.append(mag["x"])
	sense_mag.append(mag["y"])
	sense_mag.append(mag["z"])
	return sense_mag

def get_acc(sense):
	sense_acc = []
	acc = sense.get_accelerometer_raw()

	sense_acc.append(acc["x"])
	sense_acc.append(acc["y"])
	sense_acc.append(acc["z"])
	return sense_acc

def get_gyro(sense):
	sense_gyro = []
	gyro = sense.get_gyroscope_raw()

	sense_gyro.append(gyro["x"])
	sense_gyro.append(gyro["y"])
	sense_gyro.append(gyro["z"])
	return sense_gyro

def get_measurement(sense):
	row_data = []
	row_data.append(get_temp(sense))
	row_data.append(get_press(sense))
	row_data.append(get_hum(sense))
	row_data.extend(get_orientation(sense))
	row_data.extend(get_mag(sense))
	row_data.extend(get_acc(sense))
	row_data.extend(get_gyro(sense))
	return row_data

def show_msg(sense):
	global KILL_SHOW_MSG_THREAD
	print("show_msg works.")
	while not KILL_SHOW_MSG_THREAD:
		t = get_temp(sense)
		p = get_press(sense)
		h = get_hum(sense)

		t = round(t, 1)
		p = round(p, 1)
		h = round(h, 1)

		if t > 18.3 and t < 26.7:
			bg = [0, 100, 0]  # green
		else:
			bg = [100, 0, 0]  # red

		msg = "Temperature = %s, Pressure=%s, Humidity=%s" % (t, p, h)

		sense.show_message(msg, scroll_speed=0.03, back_colour=bg)

def create_header(file_name, interval_in_secs):
	date = datetime.now().strftime('%d.%m.%Y')
	time = datetime.now().strftime('%H.%M.%S')
	with open(file_name, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Time: '+date+' '+time+' '+str(interval_in_secs)])

if __name__ == '__main__':
	sense = SenseHat()
	sense.set_rotation(180)
	exit_time_in_mins = 60 * 3
	interval_in_secs = 5
	file_name = 'data 01.csv'
	thread = Thread(target=show_msg, args=(sense,))
	thread.start()

	loops = int(exit_time_in_mins * 60 / interval_in_secs) - 1

	create_header(file_name, interval_in_secs)

	for loop in range(0, loops):
		with open(file_name, 'a', newline='') as file:
			writer = csv.writer(file)
			row_data = get_measurement(sense)
			writer.writerow(row_data)

			print('Data: '+str(loop+1)+'/'+str(loops), end = ' ')
			print(row_data)

			sleep(interval_in_secs)
	print("Exited correctly. Shutting down the program.")
	print("End time:", datetime.now().strftime('%H:%M:%S'))
	KILL_SHOW_MSG_THREAD = True
