class SolidExchange:

    def __init__(self, prev_bloc=None, next_bloc=None, radiations=False, prev_temp_radiation=None, next_temp_radiation=None):
        """
            :param h: parametre de conducto-convection
        """

        self.radiations = radiations
        self.prev_bloc = prev_bloc
        self.next_bloc = next_bloc

        self.prev_temp_radiation = prev_temp_radiation
        self.next_temp_radiation = next_temp_radiation

    @property
    def h(self):
        if self.prev_bloc is None or self.next_bloc is None:
            return 0

        e1, lambda_1, S1 = self.prev_bloc.x(), self.prev_bloc.thermal_conductivity(), self.prev_bloc.S
        e2, lambda_2, S2 = self.next_bloc.x(), self.next_bloc.thermal_conductivity(), self.next_bloc.S

        # if self.convection :
        #     return 1 / ((e1 / (2 * lambda_1 * S1)) + (e2 / (2 * lambda_2 * S2))) + self.h1*S1 + self.h2*S2

        return 1 / ((e1 / (2 * lambda_1 * S1)) + (e2 / (2 * lambda_2 * S2)))



