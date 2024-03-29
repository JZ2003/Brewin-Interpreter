class Bnull:
    def __init__(self,className=None):
        """
        If the className is None, it's a generic null.
        Otherwise, it has a list of types (including the supers).
        """
        self.className = className
        
    def get_type(self):
        return self.className
    
    def change_type(self,className):
        self.className = className