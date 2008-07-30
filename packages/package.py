# -*- coding: utf-8 -*-
from zope.interface import implements

from seishub.util.text import validate_id, to_uri, to_xpath_query
from seishub.db.util import Serializable, Relation
from seishub.packages.interfaces import IPackageWrapper, IResourceTypeWrapper
from seishub.packages.defaults import schema_tab, stylesheet_tab, alias_tab,\
                                      packages_tab, resourcetypes_tab

class PackageWrapper(Serializable):
    """Wrapped around packages for storage in database."""
    
    implements(IPackageWrapper)
    
    db_table = packages_tab
    db_mapping = {'package_id':'name',
                  'version':'version',
                  '_id':'id'
                  } 
    
    def __init__(self, package_id = None, version = ''):
        self.package_id = package_id
        self.version = version
        
    def __str__(self):
        return self.package_id + '/' + self.version
        
    def setPackage_id(self, package_id):
        self._package_id = validate_id(package_id)
        
    def getPackage_id(self):
        return self._package_id
    
    package_id = property(getPackage_id, setPackage_id, 
                          "unique package id (string)")
    
    def setVersion(self, version):
        version = version or ''
        if not isinstance(version, basestring):
            raise TypeError("Version must be a string.")
        self._version = version
    
    def getVersion(self):
        return self._version
    
    version = property(getVersion, setVersion, 'version of package')

class ResourceTypeWrapper(Serializable):
    """Wrapped around resource types for storage in database."""
    
    implements(IResourceTypeWrapper)
    
    db_table = resourcetypes_tab
    db_mapping = {'resourcetype_id':'name',
                  'package':Relation(PackageWrapper,'package_id'),
                  'version':'version',
                  'version_control':'version_control',
                  '_id':'id'
                  }
    
    def __init__(self, resourcetype_id = None, package = PackageWrapper(), 
                 version = '', version_control = False):
        self.resourcetype_id = resourcetype_id
        self.package = package
        self.version = version
        self.version_control = version_control
        
    def __str__(self):
        return str(self.package.package_id) + '/' +\
               str(self.resourcetype_id) + '/' + self.version
        
    def setResourcetype_id(self, id):
        self._resourcetype_id = validate_id(id)
        
    def getResourcetype_id(self):
        return self._resourcetype_id
    
    resourcetype_id = property(getResourcetype_id, setResourcetype_id, 
                               "unique package id (string)")
    
#    def getPackageId(self):
#        return self._package_id
#    
#    def setPackageId(self, data):
#        self._package_id = data
#        #self._package_id = validate_id(data)
#        
#    package_id = property(getPackageId, setPackageId, "Package id")

    def getPackage(self):
        return self._package
    
    def setPackage(self, package):
        if not IPackageWrapper.providedBy(package):
            raise TypeError('%s does not implement IPackageWrapper' %\
                             str(package))
        self._package = package
        
    package = property(getPackage, setPackage, "Package")
    
    def setVersion(self, version):
        version = version or ''
        if not isinstance(version, basestring):
            raise TypeError("Version must be a string.")
        self._version = version
    
    def getVersion(self):
        return self._version
    
    version = property(getVersion, setVersion, 'version of package')
    
    def setVersion_control(self, value):
        if not isinstance(value, bool):
            raise TypeError("Version_control must be boolean.")
        self._version_control = value
        
    def getVersion_control(self):
        return self._version_control
    
    version_control = property(getVersion_control, setVersion_control, 
                            'Boolean indicating if version control is enabled')
    

class Alias(Serializable):
    db_table = alias_tab
    db_mapping = {'resourcetype':Relation(ResourceTypeWrapper, 
                                             'resourcetype_id'),
                  'package':Relation(PackageWrapper, 'package_id'),
                  'name':'name',
                  'expr':'expr'
                  }
    
    def __init__(self, package = PackageWrapper(), 
                 resourcetype = ResourceTypeWrapper(),
                 name = None, expr = None):
        super(Serializable, self).__init__()
        self.package = package
        self.resourcetype = resourcetype
        self.name = name
        self.expr = expr
    
    def __str__(self):
        return to_uri(self.package.package_id, 
                      self.resourcetype.resourcetype_id) + '/@' + self.name
    
    def getResourceType(self):
        return self._resourcetype
     
    def setResourceType(self, data):
        if data and not IResourceTypeWrapper.providedBy(data):
            raise TypeError("%s is not an IResourceTypeWrapper" % str(data))
        self._resourcetype = data
        
    resourcetype = property(getResourceType, setResourceType, "Resource type")
    
    def getPackage(self):
        return self._package
    
    def setPackage(self, data):
        if data and not IPackageWrapper.providedBy(data):
            raise TypeError("%s is not an IPackageWrapper" % str(data))
        self._package = data
        
    package = property(getPackage, setPackage, "Package")
    
    def getName(self):
        return self._name
    
    def setName(self, data):
        if data is not None and not isinstance(data, basestring):
            raise TypeError("Invalid alias name, String expected: %s" % data)
        self._name = validate_id(data)
        
    name = property(getName, setName, "Name of the alias")
    
    def getExpr(self):
        return self._expr
    
    def setExpr(self, data):
        if data is not None and not isinstance(data, basestring):
            raise TypeError("Invalid alias expression, String expected: %s" %\
                             data)
        self._expr = data
    
    expr = property(getExpr, setExpr, "Alias expression (XPath query)")
    
    def getQuery(self):
        """return query string"""
        return to_xpath_query(self.package.package_id, 
                              self.resourcetype.resourcetype_id, self._expr)

class Schema(Serializable):
    db_table = schema_tab
    db_mapping = {'resourcetype':Relation(ResourceTypeWrapper, 
                                          'resourcetype_id'),
                  'package':Relation(PackageWrapper,
                                     'package_id'),
                  'type':'type',
                  'resource_id':'resource_id'
                  }
    
    def __init__(self, package = PackageWrapper(), 
                 resourcetype = ResourceTypeWrapper(), 
                 type = None, resource_id = None):
        super(Serializable, self).__init__()
        self.package = package
        self.resourcetype = resourcetype
        self.type = type
        self.resource_id = resource_id
        
    def __str__(self):
        return to_uri(self.package.package_id, 
                      self.resourcetype.resourcetype_id) + '/' + self.type
    
    def getResourceType(self):
        return self._resourcetype
     
    def setResourceType(self, data):
        if data and not IResourceTypeWrapper.providedBy(data):
            raise TypeError("%s is not an IResourceTypeWrapper" % str(data))
        self._resourcetype = data
        
    resourcetype = property(getResourceType, setResourceType, "Resource type")
    
    def getPackage(self):
        return self._package
    
    def setPackage(self, data):
        if data and not IPackageWrapper.providedBy(data):
            raise TypeError("%s is not an IPackageWrapper" % str(data))
        self._package = data
        
    package = property(getPackage, setPackage, "Package")
    
    def getResource_id(self):
        return self._resource_id
    
    def setResource_id(self, data):
        self._resource_id = data
        
    resource_id = property(getResource_id, setResource_id, 
                           "Unique resource identifier (integer)")
    
    def getType(self):
        return self._type
    
    def setType(self, data):
        self._type = validate_id(data)
    
    type = property(getType, setType, "Type")
    
    def getResource(self):
        # lazy resource retrieval: to avoid getting all resources in the registry
        # on every query, resources are retrieved only if really needed (and 
        # accessed via schema.resource
        if hasattr(self, '_resource'):
            return self._resource
        if not hasattr(self, '_catalog'):
            return None
        r = self._catalog.xmldb.getResource(resource_id = self.resource_id)
        self._resource = r
        return r

    resource = property(getResource, doc = "XmlResource (read only)")
    
class Stylesheet(Schema):
    db_table = stylesheet_tab