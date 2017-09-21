# translate md to html
class Translator:
	class MDgrammerRE:
		# match

		# there can not be anything else in it
		header = '#{1,6} .+$'
		hr = '---$'
		codeBlock = '```$' # must be in pairs

		# there can be the 'search-able' thing in it 
		ul = '[-+\*] .+$'
		ol = '\d+\. .+$'

		quote = '> .+$'

		tcontent = '(\|.+){2,}\|$' # both th and td
		thr = '(\| *:?-+:? *){2,}\|$' # the horizontal rule dividing head and body
		#tcol = '\|.+' # how many columes are in the table? must match

		# search
		link = '\[.*\]\(.+\)'
		img = '\!\[.*\]\(.+\)'
		# autoLink = '<.+>' # it is crash with the html tag

		strong = '\*\* .+ \*\*'
		em = '\* .+ \*'
		code = '`.+`'
	
	def __init__(self, input, output):
		self.input = input
		self.output = output
		self.go()
	
	def go(self):
		# read the md file
		file = open(self.input, 'r')
		self.lines = file.readlines()
		file.close()
		
		self.translate()
		
		# write an html file		
		newFile = open(self.output, 'w')
		newFile.writelines(self.newLines)
		newFile.close()
	
	def translate(self):
		import re
		md = self.MDgrammerRE()
		self.newLines = []
		
		i = 0
		while i < len(self.lines):
			line = self.lines[i][:-1]
			# print(line)
			newLine = line + '\n'
			
			#print(type(md.header))
			if re.match(md.header, line):
				level = re.match(r'#{1,6}', line).span()[1]
				# print(level)
				newLine = '<h' + str(level) + '>' +\
				line[level+1:] + '</h' + str(level) + '>\n'
				
			elif re.match(md.hr, line):
				newLine = '<hr>\n'
				
			elif re.match(md.codeBlock, line):
				flag = 0
				codes = []
				for j in range(i+1, len(self.lines)):
					line = self.lines[j][:-1]
					if re.match(md.codeBlock, line):
						flag = 1
						i = j
						break
					codes.append(line)
				#print(codes)
				if flag == 1:
					newLine = '<p><code>' + codes[0] + '</code></p>\n'
					for code in codes[1:]:
						newLine += '<p><code>' + code + '</code></p>\n'
						
			else:
				line = self.searchSomething(line)
				newLine = line + '\n'
				
				if re.match(md.quote, line):
					quotes = [line[2:]]
					for j in range(i+1, len(self.lines)):
						line = self.lines[j][:-1]
						if not re.match(md.quote, line):
							i = j-1
							break
						quotes.append(line[2:])
					#print(quotes)
					newLine = '<p>' + quotes[0] + '</p>\n'
					for quote in quotes[1:]:
						newLine += '<p>' + quote + '</p>\n'
					newLine = '<blockquote>\n' + newLine + '</blockquote>\n'
					
				elif re.match(md.ul, line):
					lists = [re.sub(r'[-+\*] ', '', line)]
					for j in range(i+1, len(self.lines)):
						line = self.lines[j][:-1]
						if not re.match(md.ul, line):
							i = j-1
							break
						lists.append(re.sub(r'[-+\*] ', '', line))
					# print(lists)
					newLine = '<li>' + lists[0] + '</li>\n'
					for list in lists[1:]:
						newLine += '<li>' + list + '</li>\n'
					newLine = '<ul>\n' + newLine + '</ul>\n'
				
				elif re.match(md.ol, line):
					lists = [re.sub(r'\d\. ', '', line)]
					for j in range(i+1, len(self.lines)):
						line = self.lines[j][:-1]
						if not re.match(md.ol, line):
							i = j-1
							break
						lists.append(re.sub(r'\d\. ', '', line))
					# print(lists)
					newLine = '<li>' + lists[0] + '</li>\n'
					for list in lists[1:]:
						newLine += '<li>' + list + '</li>\n'
					newLine = '<ol>\n' + newLine + '</ol>\n'
					
				elif re.match(md.tcontent, line):
					#print(line)
					flag = 0
					heads = re.sub(r'\| *', '|', line)
					heads = re.sub(r' *\|', '|', heads).split('|')[1:-1]
					#print(heads)
					tcol = len(heads)
					
					if i+1 < len(self.lines):
						line = self.lines[i+1]
					align = []
					if len(line.split('|')) == tcol + 2 and\
					re.match(md.thr, line):
						flag = 1
						line = re.sub(r'\| *', '|', line)
						line = re.sub(r' *\|', '|', line).split('|')[1:-1]
						#print(line)
						for thr in line:
							if re.match(r':-+:$', thr):
								align.append(' style="text-align:center"')
							elif re.match(r':-+$', thr):
								align.append(' style="text-align:left"')
							elif re.match(r'-+:$', thr):
								align.append(' style="text-align:right"')
							else:
								align.append('')
					#print(tcol, align)
					bodys = []
					if flag == 1:
						for j in range(i+2, len(self.lines)):
							line = self.lines[j][:-1]
							if len(line.split('|')) == tcol + 2 and\
							re.match(md.tcontent, line):
								flag = 2
								i = j
								body = re.sub(r'\| *', '|', line)
								body = re.sub(r' *\|', '|', body).split('|')[1:-1]
								bodys.append(body)
							else:
								break
					#print(bodys)
					if flag == 2:
						newLine = '<table>\n<thead>\n<tr>\n'
						for j in range(tcol):
							newLine += '<th' + align[j] +\
							'>' + heads[j] + '</th>\n'
							
						newLine += '</tr>\n</thead>\n<tbody>\n'
						
						#print(newLine)
						for body in bodys:
							#print(body)
							newLine += '<tr>\n'
							for j in range(tcol):
								newLine += '<th' + align[j] +\
								'>' + body[j] + '</th>\n'
							newLine += '</tr>\n'
							
						newLine += '</tbody>\n</table>\n' 
				
				else:
					newLine = '<p>' + newLine[:-1] + '</p>\n'

			self.newLines.append(newLine + '\n')
			i += 1
		
	def searchSomething(self, line):
		import re
		md = self.MDgrammerRE()
		#print(line)
		
		if re.search(md.code, line):
			range = re.search(md.code, line).span()
			
			code = '<code>' + line[range[0]:range[1]][1:-1] + '</code>'
			
			line = re.sub(md.code, code, line)
		
		elif re.search(md.img, line):
			range = re.search(md.img, line).span()
			
			alt = re.sub(r'\]\(.+\)', '', line[range[0]:range[1]])[2:]
			src = re.sub(r'\!\[.*\]\(', '', line[range[0]:range[1]])[:-1]
			
			a = '<div><img src="' + src + '" alt="' + alt +\
			'"><br><div>' + alt + '</div></div>'
			
			line = re.sub(md.img, a, line)
			
		elif re.search(md.link, line):
			range = re.search(md.link, line).span()
			
			text = re.sub(r'\]\(.+\)', '', line[range[0]:range[1]])[1:]
			href = re.sub(r'\[.*\]\(', '', line[range[0]:range[1]])[:-1]
			#print(text)
			
			a = '<a href="' + href + '" target="_blank">' + text + '</a>'
			line = re.sub(md.link, a, line)
			
		# elif re.search(md.autoLink, line):
			# range = re.search(md.autoLink, line).span()
			
			# href = line[range[0]:range[1]][1:-1]
			
			# a = '<a href="' + href + '" target="_blank"/>'
			# line = re.sub(md.autoLink, a, line)
			
		elif re.search(md.strong, line):
			range = re.search(md.strong, line).span()
			
			strong = '<strong>' + line[range[0]:range[1]][3:-3] + '</strong>'
			
			line = re.sub(md.strong, strong, line)
		
		elif re.search(md.em, line):
			range = re.search(md.em, line).span()
			
			em = '<em>' + line[range[0]:range[1]][2:-2] + '</em>'
			
			line = re.sub(md.em, em, line)
		
		else:
			#print(line)
			return line
			
		line = self.searchSomething(line)
		return line
	
trans = Translator('1.md', '1.html')

	

