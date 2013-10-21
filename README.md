pyhk2
=====

Python Hundred-Kilobyte Kernel library.

It is inspired by [HK2 library] for Java that allows easily create plug-in based applications.

This library provides:
* Marking classes as services and interfaces as contracts thus declaring explicitly possible extension points and their implementations
* Runtime discovery of services and contracts
* Inversion of Control (IoC) and dependency injection (DI)
* API for fine-level control over service instantiation
* Lifetime control mechanisms (scopes)
* Custom injection resolution


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
class Foo(IFoo):
	
	@inject(IBar)
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

Service registry
--------------------

Primary way of using the *pyhk2* library is by using decorator-based service discovery. This mechanism is based on using following decorators:
* **Contract** decorator - marks interface as a potential extension point
* **Service** decorator - marks class as implementation of one or many extension points

<pre>
<code>
@interface
@contract
class IReporter(object):
	def report(self):
		"""Reports some data"""

@service
class MyReporter(IReporter):
	
	@inject(ISomeDependency)
	def __init__(self, dep):
		...

habitat = Habitat()
reporters = habitat.getAllByComponent(IReporter)
for r in reporters:
	r.report()
</code>
</pre>

Example above demonstrates explicit instantiation of extensions via *Habitat*. *Habitat* is the client-side interface that represents the kernel. Habitat provides methods to look-up services manually, and explore the extension graph. You can inject *Habitat* into your services like any other service.

However, using *Habitat* explicitly is rarely needed, simpler and cleaner way to resolve the extensions by contract is to use dependency injection mechanism.

Explicit instantiation via *Habitat* is primarily useful for delayed instantiation of extensions, but in other cases prefer injection or you'll end up with *Service Locator* anti-pattern.

[HK2 library]:http://hk2.java.net