class Exchange:

    def __init__(self, prev_bloc=None, next_bloc=None, h=0.0, radiations=False, prev_temp_radiation=None, next_temp_radiation=None):
        """
            :param h: parametre de conducto-convection
        """

        self.h = h
        self.radiations = radiations

        self.prev_bloc = prev_bloc
        self.next_bloc = next_bloc

        self.prev_temp_radiation = prev_temp_radiation
        self.next_temp_radiation = next_temp_radiation
