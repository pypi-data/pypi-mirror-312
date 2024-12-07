from abc import ABC,abstractmethod
from .ReaderSchema import ReaderSchema

class GalleryReaderSchema(ReaderSchema,ABC):

  def create_image_size_atom(self):
    self.image_size_atom = self.atom_factory.createData('Max image size',30)
