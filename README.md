pyhk2
=====

Python Hundred-Kilobyte Kernel plug-in library.

Interfaces for programming to contracts
---------------------------------------

<pre>
<code>
@interface
class IFoo(object):
	def foo(self):
		'''Does foo'''

@interface
class IBar(object):

	def bar(self):
		'''Does bar'''

class FooBar(IFoo, IBar):
	def foo(self):
		return 'foo!'

>> fb = FooBar()
>> fb.foo()
foo!
>> fb.bar()
NotImplementedError: abstract method call
</code>
</pre>

Dependency injection
--------------------

<pre>
<code>
@inject(IBar)
class Foo(IFoo):
	def __init__(self, bar):
		self._bar = bar

	def foo(self):
		return 'foo ' + self._bar.bar() + ' !'

class Bar(IBar):
	def bar(self):
		return 'bar'

>> c = Container()
>> c.bind(IFoo, Foo)
>> c.bind(IBar, Bar)
>> f = c.get(IFoo)
>> f.foo()
foo bar !
</code>
</pre>