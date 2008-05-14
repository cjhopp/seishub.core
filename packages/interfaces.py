# -*- coding: utf-8 -*-

from seishub.core import Interface
from zope.interface import Attribute


class IPackage(Interface):
    """This is the main interface for a unique seishub package."""
    
    package_id = Attribute("""
        Defines the package ID of this resource.
        
        This items should return a single string with an unique package id.
        """)
    

class IResourceType(IPackage):
    """Interface definition for a unique resource type of a package."""
    
    resourcetype_id = Attribute("Defines the ID of this resource type.")


class IAliases(IPackage):
    """Interface of aliases for a package or resource type."""

    def getAliases():
        """Return dict of aliases in form of {'URL': 'XPath Query',}."""


class IStylesheets(IPackage):
    """Interface of XML stylesheets for a package or resource type."""
    
    def getStylesheets():
        """Return dict of stylesheets in form of {'output_id': 'URI',}."""


class ISchemas(IPackage):
    """Interface of XML validation schemas for a package or resource type."""
    
    def getSchemas():
        """Return URI list of validation schemas (dtd or xsd)."""


class IResourceMapper(IResourceType):
    """Interface definition for a resource mapper for SFTP and REST."""
    
    def getMappingURL():
        """
        Define an user mapped URL.
        
        The full URL consists of package_id/resourcetype_id/mapping_url. 
        """
    
    def processGET(request):
        """
        Process a GET request.
        
        This function should return a string containing a valid XML document.
        """
    
    def processPUT(request):
        """
        Process a PUT request.
        
        This function should return a string containing the new resource url.
        """
    
    def processPOST(request):
        """
        Process a POST request.
        
        This function should return a string containing the new resource url if
        the resource could be updated, otherwise a SeisHubError instance.
        """
    
    def processDELETE(request):
        """
        Process a DELETE request.
        
        This function should return True if the resource could be deleted 
        otherwise a SeisHubError instance.
        """
    