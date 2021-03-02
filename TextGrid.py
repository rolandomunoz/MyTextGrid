import re

class TextGrid:
	'''
	A TextGrid representation
	'''
	def __init__(self):
		self.xmin = 0
		self.xmax = 0
		self.size = 0
		self.tiers = []
		
	def append_tier(self, Tier):
		self.tiers.append(Tier)
		self.size = len(self.tiers)

	def update_info(self, xmin, xmax, tiers = []):
		self.xmin = xmin
		self.xmax = xmax
		self.tiers = tiers
	
class TextGridParser:
	
	def __init__(self):
		self.textgrid = TextGrid()
		
	def parse(self, path):
		self._f = open(path, 'r', encoding='utf-8')
		is_textgrid= self.is_textgrid()
		if not is_textgrid:
			raise ErrorName('The file {} is not a TextGrid'.format(path))
		self.scan_general_info()
		self.scan_tiers()
		return self.textgrid
		
	def is_textgrid(self):
		file_type = self.get_next_value()
		object_class = self.get_next_value()
		if object_class == '"TextGrid"':
			return True
		return False

	def scan_general_info(self):
		self.textgrid
		
		xmin = self.get_next_value()
		xmax = self.get_next_value()
		tier_exists = self.get_next_value()
		size = self.get_next_value()
		self.textgrid.update_info(xmin, xmax)
		
	def scan_tiers(self):
		while True:
			tier_class = self.get_next_value()
			if tier_class == None:
				return None
			if tier_class == '"IntervalTier"':
				self.scan_interval_tier()
			elif tier_class == '"TextTier"':
				self.scan_point_tier()

	def scan_interval_tier(self):
		tier_name = self.get_next_value()
		xmin = float(self.get_next_value())
		xmax = float(self.get_next_value())
		size = int(self.get_next_value())
		interval_tier = IntervalTier(tier_name, xmin, xmax)
		
		for index in range(size):
			xmin = self.get_next_value()
			xmax = self.get_next_value()
			text = self.get_next_value()
			interval_item = IntervalItem(text, xmin, xmax)
			interval_tier.append(interval_item)
		self.textgrid.append_tier(interval_tier)
		
	def scan_point_tier(self):
		tier_name = self.get_next_value()
		xmin = float(self.get_next_value())
		xmax = float(self.get_next_value())
		size = int(self.get_next_value())
		point_tier = TextTier(tier_name, xmin, xmax)

		for index in range(size):
			number = self.get_next_value()
			mark = self.get_next_value()
			point_item = PointItem(mark, number)
			point_tier.append(point_item)
		self.textgrid.append_tier(point_tier)

	def get_next_value(self):
		while True:
			raw_line = self._f.readline()
			if raw_line == '':
				return None
			if raw_line == '\n':
				continue
			if '[' in raw_line:
				continue
			if raw_line.startswith('tiers?'):
				raw_line = 'tier_status = ' + raw_line
			line = raw_line.rstrip().lstrip()
			line = line.split('= ', 1)[1]
			return line
		
class IntervalTier:

	def __init__(self, name, xmin, xmax):
		self.class_ = 'Interval tier'
		self.name = name
		self.xmin = xmin
		self.xmax = xmax
		self.size = 0
		self.intervals = list()

	def append(self, IntervalTier):
		self.intervals.append(IntervalTier)
		self.size = len(self.intervals)
		
	def update(self, name, xmin, xmax, intervals = []):
		self.name = name
		self.xmin = xmin
		self.xmax = xmax
		self.intervals = intervals
	
class TextTier:
	
	def __init__(self, name, xmin, xmax):
		self.class_ = 'Point tier'
		self.name = name
		self.xmin = xmin
		self.xmax = xmax
		self.size = 0
		self.points = list()

	def append(self, PointItem):
		self.points.append(PointItem)
		self.size = len(self.points)
		
class PointItem:
	
	def __init__(self, number, mark = ''):
		self.number = number
		self.mark = mark

class IntervalItem:
	
	def __init__(self, xmin, xmax, text = ''):
		self.xmin = xmin
		self.xmax = xmax
		self.text = text
	
if __name__ == '__main__':
	path = r'C:\Users\lab\Desktop\TextGrid\test\Mary_John_bell.TextGrid'
	#path = r'C:\Users\lab\Desktop\TextGrid\test\New Text Document.TextGrid'
	#path = r"C:\Users\lab\Desktop\TextGrid\test\000000000023975_3136566863_-_05_06_2018_at_15_49_56_695-1.TextGrid"
	tg_parser = TextGridParser()
	tg = tg_parser.parse(path)
	print(tg.xmin)
	print(tg.xmax)
	print(tg.size)
	for tier in tg.tiers:
		print(tier.name)
		print(tier.class_)