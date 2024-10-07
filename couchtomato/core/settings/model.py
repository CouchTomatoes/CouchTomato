# from elixir.fields import Field
# from elixir.options import options_defaults
# from elixir.relationships import OneToMany, ManyToOne
# from sqlalchemy.types import Integer, String, Unicode
from couchtomato import base
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

# options_defaults["shortnames"] = True

# We would like to be able to create this schema in a specific database at
# will, so we can test it easily.
# Make elixir not bind to any session to make this possible.
#
# http://elixir.ematia.de/trac/wiki/Recipes/MultipleDatabasesOneMetadata
# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
__session__ = None
class Resource(base):
    """Represents a resource of movies.  This recources can be online or
    offline."""
    __tablename__ = 'Resource'
    resourceid = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    releases = relationship('Release', backref = 'Resource')

    def __init__(self, name, path):
        self.name = name
        self.path = path
class Release(base):
    """Logically groups all files that belong to a certain release, such as
    parts of a movie, subtitles, nfo, trailers etc."""
    __tablename__ = 'Release'
    releaseid = Column(Integer, primary_key=True)
    resourceid = Column(Integer, ForeignKey('Resource.resourceid'))
    resource = relationship('Resource')
    files = relationship('File', backref = 'Release')
    
class File(base):
    """File that belongs to a release."""
    __tablename__ = 'File'
    fileid = Column(Integer, primary_key=True)
    histories = relationship('RenameHistory', backref = 'File')
    path = Column(String, nullable = False, unique = True)
    # Subtitles can have multiple parts, too
    part = Column(Integer)
    releaseid = Column(Integer, ForeignKey('Release.releaseid'))
    # Let's remember the size so we know about offline media.
    size = Column(Integer, nullable = False)
    filetypeid = Column(Integer, ForeignKey('FileType.filetypeid'))
    filetypes = relationship('FileType')
    
class FileType(base):
    """Types could be trailer, subtitle, movie, partial movie etc."""
    __tablename__ = 'FileType'
    filetypeid = Column(Integer, primary_key=True)
    identifier = Column(String(20), unique = True)
    name = Column(String, nullable = False)
    files = relationship('File', backref = 'FileType')

class RenameHistory(base):
    """Remembers from where to where files have been moved."""
    __tablename__ = 'RenameHistory'
    renamehistoryid = Column(Integer, primary_key=True)
    old = Column(String(255))
    new = Column(String(255))
    fileid = Column(Integer, ForeignKey('File.fileid'))