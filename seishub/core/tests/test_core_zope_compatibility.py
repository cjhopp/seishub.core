# -*- coding: utf-8 -*-

"""Test Interface implementation adopted from zope test suite. Interface and 
implements declaration is taken from seishub.core."""

##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################


import unittest

from zope.interface.exceptions import BrokenImplementation, Invalid
from zope.interface import implementedBy, providedBy, invariant
from zope.interface import directlyProvides, Attribute

from seishub.core.core import Interface, implements


class mytest(Interface):
    pass

class C(object):
    def m1(self, a, b): #@UnusedVariable
        "return 1"
        return 1

    def m2(self, a, b): #@UnusedVariable
        "return 2"
        return 2

# testInstancesOfClassImplements

#  YAGNI IC=Interface.impliedInterface(C)
class IC(Interface):
    def m1(a, b): #@NoSelf
        "return 1"

    def m2(a, b): #@NoSelf
        "return 2"



C.__implemented__ = IC

class I1(Interface):
    def ma(): #@NoSelf
        "blah"

class I2(I1): pass

class I3(Interface): pass

class I4(Interface): pass

class A(I1.deferred()):
    implements(I1)

class B(object):
    implements(I2, I3)

class D(A, B): pass

class E(A, B):
    __implemented__ = A.__implemented__, C.__implemented__


class FooInterface(Interface):
    """ This is an Abstract Base Class """

    foobar = Attribute("fuzzed over beyond all recognition")

    def aMethod(foo, bar, bingo): #@NoSelf
        """ This is aMethod """

    def anotherMethod(foo=6, bar="where you get sloshed", bingo=(1, 3,)): #@NoSelf
        """ This is anotherMethod """

    def wammy(zip, *argues): #@NoSelf
        """ yadda yadda """

    def useless(**keywords): #@NoSelf
        """ useless code is fun! """

class Foo(object):
    """ A concrete class """

    implements(FooInterface)

    foobar = "yeah"

    def aMethod(self, foo, bar, bingo): #@UnusedVariable
        """ This is aMethod """
        return "barf!"

    def anotherMethod(self, foo=6, bar="where you get sloshed", bingo=(1, 3,)): #@UnusedVariable
        """ This is anotherMethod """
        return "barf!"

    def wammy(self, zip, *argues): #@UnusedVariable
        """ yadda yadda """
        return "barf!"

    def useless(self, **keywords): #@UnusedVariable
        """ useless code is fun! """
        return "barf!"

foo_instance = Foo()

class Blah(object):
    pass

new = Interface.__class__
FunInterface = new('FunInterface')
BarInterface = new('BarInterface', [FunInterface])
BobInterface = new('BobInterface')
BazInterface = new('BazInterface', [BobInterface, BarInterface])

# fixtures for invariant tests
def ifFooThenBar(obj):
    if getattr(obj, 'foo', None) and not getattr(obj, 'bar', None):
        raise Invalid('If Foo, then Bar!')
class IInvariant(Interface):
    foo = Attribute('foo')
    bar = Attribute('bar; must eval to Boolean True if foo does')
    invariant(ifFooThenBar)
def BarGreaterThanFoo(obj):
    foo = getattr(obj, 'foo', None)
    bar = getattr(obj, 'bar', None)
    if foo is not None and isinstance(foo, type(bar)):
        # type checking should be handled elsewhere (like, say, 
        # schema); these invariants should be intra-interface 
        # constraints.  This is a hacky way to do it, maybe, but you
        # get the idea
        if not bar > foo:
            raise Invalid('Please, Boo MUST be greater than Foo!')
class ISubInvariant(IInvariant):
    invariant(BarGreaterThanFoo)
class InvariantC(object):
    pass



class ZopeCompatibilityTestCase(unittest.TestCase):

    def testInterfaceSetOnAttributes(self):
        self.assertEqual(FooInterface['foobar'].interface,
                         FooInterface)
        self.assertEqual(FooInterface['aMethod'].interface,
                         FooInterface)

    def testClassImplements(self):
        self.assert_(IC.implementedBy(C))

        self.assert_(I1.implementedBy(A))
        self.assert_(I1.implementedBy(B))
        self.assert_(not I1.implementedBy(C))
        self.assert_(I1.implementedBy(D))
        self.assert_(I1.implementedBy(E))

        self.assert_(not I2.implementedBy(A))
        self.assert_(I2.implementedBy(B))
        self.assert_(not I2.implementedBy(C))

        # No longer after interfacegeddon
        # self.assert_(not I2.implementedBy(D))

        self.assert_(not I2.implementedBy(E))

    def testUtil(self):
        self.assert_(IC in implementedBy(C))
        self.assert_(I1 in implementedBy(A))
        self.assert_(not I1 in implementedBy(C))
        self.assert_(I2 in implementedBy(B))
        self.assert_(not I2 in implementedBy(C))

        self.assert_(IC in providedBy(C()))
        self.assert_(I1 in providedBy(A()))
        self.assert_(not I1 in providedBy(C()))
        self.assert_(I2 in providedBy(B()))
        self.assert_(not I2 in providedBy(C()))


    def testObjectImplements(self):
        self.assert_(IC.providedBy(C()))

        self.assert_(I1.providedBy(A()))
        self.assert_(I1.providedBy(B()))
        self.assert_(not I1.providedBy(C()))
        self.assert_(I1.providedBy(D()))
        self.assert_(I1.providedBy(E()))

        self.assert_(not I2.providedBy(A()))
        self.assert_(I2.providedBy(B()))
        self.assert_(not I2.providedBy(C()))

        # Not after interface geddon
        # self.assert_(not I2.providedBy(D()))

        self.assert_(not I2.providedBy(E()))

    def testDeferredClass(self):
        a = A()
        self.assertRaises(BrokenImplementation, a.ma)


    def testInterfaceExtendsInterface(self):
        self.assert_(BazInterface.extends(BobInterface))
        self.assert_(BazInterface.extends(BarInterface))
        self.assert_(BazInterface.extends(FunInterface))
        self.assert_(not BobInterface.extends(FunInterface))
        self.assert_(not BobInterface.extends(BarInterface))
        self.assert_(BarInterface.extends(FunInterface))
        self.assert_(not BarInterface.extends(BazInterface))

    def testVerifyImplementation(self):
        from zope.interface.verify import verifyClass
        self.assert_(verifyClass(FooInterface, Foo))
        self.assert_(Interface.providedBy(I1))

    def test_names(self):
        names = list(_I2.names()); names.sort()
        self.assertEqual(names, ['f21', 'f22', 'f23'])
        names = list(_I2.names(all=True)); names.sort()
        self.assertEqual(names, ['a1', 'f11', 'f12', 'f21', 'f22', 'f23'])

    def test_namesAndDescriptions(self):
        names = [nd[0] for nd in _I2.namesAndDescriptions()]; names.sort()
        self.assertEqual(names, ['f21', 'f22', 'f23'])
        names = [nd[0] for nd in _I2.namesAndDescriptions(1)]; names.sort()
        self.assertEqual(names, ['a1', 'f11', 'f12', 'f21', 'f22', 'f23'])

        for name, d in _I2.namesAndDescriptions(1):
            self.assertEqual(name, d.__name__)

    def test_getDescriptionFor(self):
        self.assertEqual(_I2.getDescriptionFor('f11').__name__, 'f11')
        self.assertEqual(_I2.getDescriptionFor('f22').__name__, 'f22')
        self.assertEqual(_I2.queryDescriptionFor('f33', self), self)
        self.assertRaises(KeyError, _I2.getDescriptionFor, 'f33')

    def test___getitem__(self):
        self.assertEqual(_I2['f11'].__name__, 'f11')
        self.assertEqual(_I2['f22'].__name__, 'f22')
        self.assertEqual(_I2.get('f33', self), self)
        self.assertRaises(KeyError, _I2.__getitem__, 'f33')

    def test___contains__(self):
        self.failUnless('f11' in _I2)
        self.failIf('f33' in _I2)

    def test___iter__(self):
        names = list(iter(_I2))
        names.sort()
        self.assertEqual(names, ['a1', 'f11', 'f12', 'f21', 'f22', 'f23'])

    def testAttr(self):
        description = _I2.getDescriptionFor('a1')
        self.assertEqual(description.__name__, 'a1')
        self.assertEqual(description.__doc__, 'This is an attribute')

    def testFunctionAttributes(self):
        # Make sure function attributes become tagged values.
        meth = _I1['f12']
        self.assertEqual(meth.getTaggedValue('optional'), 1)

    def testInvariant(self):
        # set up
        o = InvariantC()
        directlyProvides(o, IInvariant)
        # a helper
        def errorsEqual(self, o, error_len, error_msgs, interface=None):
            if interface is None:
                interface = IInvariant
            self.assertRaises(Invalid, interface.validateInvariants, o)
            e = []
            try:
                interface.validateInvariants(o, e)
            except Invalid, error:
                self.assertEquals(error.args[0], e)
            else:
                self._assert(0) # validateInvariants should always raise 
                # Invalid
            self.assertEquals(len(e), error_len)
            msgs = [error.args[0] for error in e]
            msgs.sort()
            for msg in msgs:
                self.assertEquals(msg, error_msgs.pop(0))
        # the tests
        self.assertEquals(IInvariant.getTaggedValue('invariants'),
                          [ifFooThenBar])
        self.assertEquals(IInvariant.validateInvariants(o), None)
        o.bar = 27
        self.assertEquals(IInvariant.validateInvariants(o), None)
        o.foo = 42
        self.assertEquals(IInvariant.validateInvariants(o), None)
        del o.bar
        errorsEqual(self, o, 1, ['If Foo, then Bar!'])
        # nested interfaces with invariants:
        self.assertEquals(ISubInvariant.getTaggedValue('invariants'),
                          [BarGreaterThanFoo])
        o = InvariantC()
        directlyProvides(o, ISubInvariant)
        o.foo = 42
        # even though the interface has changed, we should still only have one 
        # error.
        errorsEqual(self, o, 1, ['If Foo, then Bar!'], ISubInvariant)
        # however, if we set foo to 0 (Boolean False) and bar to a negative 
        # number then we'll get the new error
        o.foo = 2
        o.bar = 1
        errorsEqual(self, o, 1, ['Please, Boo MUST be greater than Foo!'],
                    ISubInvariant)
        # and if we set foo to a positive number and boo to 0, we'll
        # get both errors!
        o.foo = 1
        o.bar = 0
        errorsEqual(self, o, 2, ['If Foo, then Bar!',
                                 'Please, Boo MUST be greater than Foo!'],
                    ISubInvariant)
        # for a happy ending, we'll make the invariants happy
        o.foo = 1
        o.bar = 2
        self.assertEquals(IInvariant.validateInvariants(o), None) # woohoo
        # now we'll do two invariants on the same interface, 
        # just to make sure that a small
        # multi-invariant interface is at least minimally tested.
        o = InvariantC()
        directlyProvides(o, IInvariant)
        o.foo = 42
        old_invariants = IInvariant.getTaggedValue('invariants')
        invariants = old_invariants[:]
        invariants.append(BarGreaterThanFoo) # if you really need to mutate,
        # then this would be the way to do it.  Probably a bad idea, though. :-)
        IInvariant.setTaggedValue('invariants', invariants)
        #
        # even though the interface has changed, we should still only have one 
        # error.
        errorsEqual(self, o, 1, ['If Foo, then Bar!'])
        # however, if we set foo to 0 (Boolean False) and bar to a negative 
        # number then we'll get the new error
        o.foo = 2
        o.bar = 1
        errorsEqual(self, o, 1, ['Please, Boo MUST be greater than Foo!'])
        # and if we set foo to a positive number and boo to 0, we'll
        # get both errors!
        o.foo = 1
        o.bar = 0
        errorsEqual(self, o, 2, ['If Foo, then Bar!',
                                 'Please, Boo MUST be greater than Foo!'])
        # for another happy ending, we'll make the invariants happy again
        o.foo = 1
        o.bar = 2
        self.assertEquals(IInvariant.validateInvariants(o), None) # bliss
        # clean up
        IInvariant.setTaggedValue('invariants', old_invariants)

    def testIssue228(self):
        # Test for http://collector.zope.org/Zope3-dev/228
        class I(Interface):
            "xxx"
        class Bad:
            __providedBy__ = None
        # Old style classes don't have a '__class__' attribute
        self.failUnlessRaises(AttributeError, I.providedBy, Bad)


class _I1(Interface):

    a1 = Attribute("This is an attribute")

    def f11(): pass #@NoSelf
    def f12(): pass #@NoSelf
    f12.optional = 1

class _I1_(_I1): pass
class _I1__(_I1_): pass

class _I2(_I1__):
    def f21(): pass #@NoSelf
    def f22(): pass #@NoSelf
    f23 = f22


def suite():
    return unittest.makeSuite(ZopeCompatibilityTestCase, 'test')


if __name__ == '__main__':
    unittest.main()
