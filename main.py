

# Apagar Dicionarios
# https://pt.stackoverflow.com/questions/355886/eliminar-valor-de-um-dicion%C3%A1rio-em-python

# Instrospecção em Python
# http://ptcomputador.com/P/python-programming/93814.html

# Obter módulos instalados localmente
# https://stackoverflow.com/questions/739993/how-can-i-get-a-list-of-locally-installed-python-modules

import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.config import Config
Config.set('graphics', 'width', str('400'))
Config.set('graphics', 'height', str('500'))

Builder.load_string('''
#:import utils kivy.utils

#:set cor_fundo1 utils.get_color_from_hex('#d35400')
#:set cor_fundo2 utils.get_color_from_hex('#f39c12')
#:set cor_fundo3 utils.get_color_from_hex('#2980b9')

#:set cor_botao utils.get_color_from_hex('#3498db')

<Home>:
	BoxLayout:
		orientation: 'vertical'
		spacing: 10
		padding: 10
		canvas.before:
			Color: 
				rgba: cor_fundo1
			RoundedRectangle:
				size: self.size
				pos: self.pos
			Color: 
				rgba: cor_fundo2
			RoundedRectangle:
				size: self.size[0] - 12, self.size[1] - 12
				pos: self.pos[0] + 6, self.pos[1] + 6
		BoxLayout:
			size_hint: 1, .15
			TextInput:
				id: pesquisar_algo
				text_size: self.size
				font_size: sp('28')
				halign: 'center'
				valign: 'center'
				on_text:
					root.pesquisar_algo()
			Button:
				id: modo
				text: 'P'
				font_size: sp('30')
				size_hint: .2, 1
				background_color: cor_botao
				background_normal: ''
				on_release:
					modo.text = 'P' if self.text == 'M' else 'M'
					root.pesquisar_algo()
		ScrollView:
			do_scroll_x: False
			do_scroll_y: True
			BoxLayout:
				id: container
				orientation: 'vertical'
				size_hint_y: None
				height: self.minimum_height
				padding: 10, 10
				spacing: dp('10')
''')

class Home(BoxLayout):
	dynamic_ids = dict()
		
	def pesquisar_pacotes(self):
		import pkg_resources
		pacotes = pkg_resources.working_set
		pacotes_instalados = sorted(["%s" % i.key for i in pacotes])
		return pacotes_instalados

	def pesquisar_metodos(self):
		metodos = None
		try:
			pacote = __import__(self.ids.pesquisar_algo.text)
			metodos = sorted(dir(pacote))
			return metodos
		except:
			return ['Pacote Inexistente']

	def pesquisar_algo(self):
		if self.ids.modo.text == 'P':
			pacotes = self.pesquisar_pacotes()
			if pacotes == None:
				print('Pacote vazio')
			else:
				itens = [x for x in pacotes if self.ids.pesquisar_algo.text in x] #Cria lista com conteúdo pesquisado
				self.atualiza_container(self.ids.container, itens) # Chama método da classe
				self.atualiza_texto(itens)
		elif self.ids.modo.text == 'M':
			metodos = self.pesquisar_metodos()
			self.atualiza_container(self.ids.container, metodos)
			self.atualiza_texto(metodos)

	"""Cria botoes dinamicos dentro de um container com uma determinada lista"""
	def atualiza_container(self, container, lista):
		container.clear_widgets()

		{k:v for k,v in self.dynamic_ids.items() if v}

		for i in lista:
			codigo = i[:3]
			bt = Builder.load_string(f'''
BoxLayout:
	id: box{codigo}
	orientation: 'vertical'
	size_hint: 1, None
	height: bl{codigo}.height + tg{codigo}.height
	ToggleButton:
		id: tg{codigo}
		text: '{i}'
		size_hint: 1,None
		height: dp('40')
		background_color: cor_botao
		background_normal: ''
		on_state:
			bl{codigo}.opacity = 0 if tg{codigo}.state == 'normal' else 1
			bl{codigo}.height = 0 if tg{codigo}.state == 'normal' else 200
	BoxLayout:
		id: bl{codigo}
		size_hint: 1, None
		height: 0
		opacity: 0
		canvas.before:
			Color:
				rgba: cor_fundo3
			Rectangle:
				size: self.size
				pos: self.pos
		Label:
			id: pergunta{codigo}
			text: '{i}'
			font_size: sp('30')
			text_size: self.size
			valign: 'middle'
			halign: 'center'
''')
			container.add_widget(bt)
			self.dynamic_ids[codigo] = bt

	def atualiza_texto(self, lista):
		for i in lista:
			codigo = i[:3]
			self.dynamic_ids[codigo].ids['pergunta'+codigo].text = str(type(i))

class MyApp(App):
	title = "Verificador de Pacotes"
	def build(self):
		return Home()

if __name__ == '__main__':
	MyApp().run()
