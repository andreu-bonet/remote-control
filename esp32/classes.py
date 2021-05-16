from machine import Pin


class PrecisionStepper:
	def __init__(self, step_pin, dir_pin, en_pin, step_time=1000, steps_per_rev=1600):
		self.stp = Pin(step_pin, Pin.OUT)
		self.dir = Pin(dir_pin, Pin.OUT)
		self.en = Pin(en_pin, Pin.OUT, value=0)

		self.step_time = step_time
		self.steps_per_rev = steps_per_rev

	def power_on(self):
		self.en.value(0)

	def power_off(self):
		self.en.value(1)

	def set_dir(self, _dir):
		self.dir.value(_dir)

	def steps(self, step_count):
		for i in range(abs(step_count)):
			self.stp.value(1)
			thime.sleep_us(self.step_time)
			self.stp.value(0)
			thime.sleep_us(self.step_time)

	def mm(self, mm, step_per_mm):
		self.steps(mm * step_per_mm)

	def set_step_time(self, us):
		self.step_time = us
