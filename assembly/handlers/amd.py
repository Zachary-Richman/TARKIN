class Amd:
    def __init__(self):
        pass

    def _compute_amd(self, sim: rebound.Simulation) -> float:
        """
        Compute the Angular Momentum Deficit (AMD) of all non-star planets

        AMD Definition (Laskar & Petit, 2017): TODO: cite, maybe include Laskar 1997
            C = sum over k of:
                lambda_k * (1 - sqrt(1 - e_k^2) * cos(i_k))
            where,
                lambda_k = m_k * sqrt(M_star * G * a_k)


        :param sim: Simulation at desired snapshot, must have called integrator_synchronize() prior to calling
        :return: AMD in rebound units (G = 1)

        Notes
        This function computes AMD over all non-star particles, including the
        outer giant if present. To isolate inner system AMD, pass a simulation
        built with outer_giant=None.
        """

