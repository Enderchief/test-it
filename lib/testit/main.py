__all__ = ["test", "Test"]

from colored import fg, bg, attr
from typing import Any, Callable, Union
import re
from time import perf_counter

def _wrap(value: Any, quote=True):
	if isinstance(value, (str)) and quote:
		value = '"value"'
	elif isinstance(value, list):
		return f'[{", ".join(_wrap(i) for i in value)}]'
	return f'{fg("yellow")}{str(value)}{attr(0)}'

class Test:
	def __init__(self, test_function: Callable[[Any], Any], description: str = None):
		self.description = description
		self.test_function = test_function
		self._tests = []

	def __call__(self):
		start = perf_counter()
		out = self.test_function(self)
		end = perf_counter() - start
		is_pass = True
			
		if False in [i['passed'] for i in self._tests]:
			is_pass = False
		
		return self._tests, is_pass, self.description

	def __str__(self):
		return f'Test {self.description}'


	def expect(self, _func: Callable[[Any], Any], *args, **kwargs):
		pos_args = ', '.join(_wrap(i) for i in args)
		keyword_args = ', '.join(f'{k}={_wrap(v)}' for k, v in kwargs.items())
		args_str = f'{pos_args}, {keyword_args}' if pos_args and keyword_args else pos_args or keyword_args 

		self._tests.append({'func': _func, 'args': args, 'kwargs': kwargs, 'args_str': args_str})
		return self


	def message(self, message: str):
		self._tests[-1]['message'] = message

	def _base_test(self, choice: str, value: str = None):
		if isinstance(self._tests[-1], dict) and ('func' in self._tests[-1]):
			args = self._tests[-1]['args']
			kwargs = self._tests[-1]['kwargs']
			func = self._tests[-1]['func']

			if callable(func):
				recieved = func(*args, **kwargs)
				self._tests[-1]['recieved'] = recieved
				self._tests[-1]['callable'] = True
			else:
				recieved = func

			if choice == 'equal':
				self._tests[-1]['passed'] = recieved == value
				expected = f'== {_wrap(value)}'
			elif choice == 'not_equal':
				self._tests[-1]['passed'] = recieved != value
				expected = f'!= {_wrap(value)}'
			elif choice == 'truthy':
				self._tests[-1]['passed'] = bool(recieved)
				expected = 'is truthy'
			elif choice == 'falsy':
				self._tests[-1]['passed'] = not bool(recieved)
				expected = 'is falsy'
			elif choice == 'empty':
				self._tests[-1]['passed'] = len(recieved) == 0
				expected = 'is empty'
			elif choice == 'not_empty':
				self._tests[-1]['passed'] = len(recieved) > 0
				expected = 'is not empty'
			elif choice == 'greater_than':
				self._tests[-1]['passed'] = recieved > value
				expected = f'is greater than {_wrap(value)}'
			elif choice == 'less_than':
				self._tests[-1]['passed'] = recieved < value
				expected = f'is less than {_wrap(value)}'
			elif choice == 'greater_than_or_equal':
				self._tests[-1]['passed'] = recieved >= value
				expected = f'is greater than or equal to {value}'
			elif choice == 'less_than_or_equal':
				self._tests[-1]['passed'] = recieved <= value
				expected = f'is less than or equal to {_wrap(value)}'
			elif choice == 'regex':
				self._tests[-1]['passed'] = re.match(value, recieved)
				expected = f'matches regex {_wrap(value)}'
			elif choice == 'not_regex':
				self._tests[-1]['passed'] = not re.match(value, recieved)
				expected = f'does not match regex {value}'
			elif choice == 'contains':
				self._tests[-1]['passed'] = value in recieved
				expected = f'contains {_wrap(value)}'
			elif choice == 'not_contains':
				self._tests[-1]['passed'] = value not in recieved
				expected = f'({self._tests[-1]["args_str"]}) does not contain {_wrap(value)}'

			else:
				raise ValueError(f'{choice} is not a valid test type')

			if callable(func):
				self._tests[-1]['name'] = func.__name__
			else:
				self._tests[-1]['name'] = _wrap(str(type(func)), quote=False)

			self._tests[-1] |= {'recieved': _wrap(recieved), 'expected': f'{fg("white")}{expected}'}
			return self
		else:
			raise ValueError("No tests have been added to this Test instance.")

	def equal(self, value: Any):
		return self._base_test('equal', value)

	def not_equal(self, value: Any):
		return self._base_test('not_equal', value)
	
	def truthy(self):
		return self._base_test('truthy')

	def falsy(self):
		return self._base_test('falsy')

	def empty(self):
		return self._base_test('empty')

	def not_empty(self):
		return self._base_test('not_empty')

	def greater_than(self, value: Any):
		return self._base_test('greater_than', value)

	def less_than(self, value: Any):
		return self._base_test('less_than', value)

	def greater_than_or_equal(self, value: Any):
		return self._base_test('greater_than_or_equal', value)

	def less_than_or_equal(self, value: Any):
		return self._base_test('less_than_or_equal', value)

	def regex(self, value: Union[str, re.Pattern]):
		if isinstance(value, str):
			value = re.compile(value)
		return self._base_test('regex', value)

	def contains(self, value: Any):
		return self._base_test('contains', value)

	def not_contains(self, value: Any):
		return self._base_test('not_contains', value)
		


def test(description: str):
	def wrapper(func: Callable[['Test'], Any]):
		return Test(func, description)
	return wrapper


