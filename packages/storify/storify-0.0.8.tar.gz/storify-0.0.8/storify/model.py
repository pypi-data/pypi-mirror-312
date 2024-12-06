class Model:
    @classmethod
    def _keyname(cls):
        """
        This method is used to get the key name for the model.
        By default, it returns the class name with double underscores prepended and appended.
        You can override this method in your model to customize the key name.
        """
        return f"__{cls.__name__}__"
    
    def _to_dict(self):
        """
        This method is used to convert the model instance to a dictionary.
        By default, it returns a dictionary of all the instance's attributes
        that do not start with an underscore.
        """
        filtered_dict = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return filtered_dict

    def _from_dict(self, data):
        """
        This method is used to convert a dictionary to a model instance.
        By default, it updates the instance's attributes with the values from
        the dictionary.
        """
        self.__dict__.update(data)
        return self

    @classmethod
    def _deserialize(cls, data):
        """
        This method is used to convert a dictionary to a model instance.
        By default, it uses the _from_dict method to convert the dictionary to an instance.
        """
        return cls._from_dict(data)
