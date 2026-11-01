# T.A.R.K.I.N.
### Trajectory Analysis and Resonance Klassifier for Inner N-body Systems

---

Planetary systems are gravitationally coupled many-body systems whose long-term evolution depends upon the masses, orbital configurations, and relative separations of their constituent bodies. Although an individual planet may initially occupy a seemingly stable orbit, gravitational interactions between multiple planets can produce cumulative changes in orbital elements over sufficiently long timescales. Consequently, stability is not solely a property of an individual orbit, but can emerge from the collective dynamical architecture of the system.

Compact planetary systems are particularly useful for investigating this behaviour because their planets occupy relatively closely spaced orbits, increasing the significance of mutual gravitational interactions. As the number of planets increases, the number of pairwise interactions also increases. However, the relationship between multiplicity and stability is not necessarily represented by a simple increase or decrease in instability, because the outcome depends upon the complete orbital configuration.

An external gravitational perturber provides another mechanism through which the stability of an initially compact system can be modified. By introducing an additional massive body outside the planetary system, the internal planets are subjected to an additional gravitational influence while their initial conditions can otherwise remain unchanged. This permits the effect of the external perturbation to be investigated as a function of planetary multiplicity.

### Research Question

> How does the number of planets in a compact planetary system affect the fraction of systems that remain stable over a fixed time interval following the introduction of an additional outer gravitational perturber at a larger semi-major axis and constant mass?

---

## Methodology

T.A.R.K.I.N. (*Trajectory Analysis and Resonance Klassifier for Inner N-body Systems*) was developed specifically for this investigation to generate and analyze ensembles of gravitationally interacting planetary systems.

Rather than evaluating the stability of a single predefined planetary configuration, the framework produces randomized systems according to controlled initial conditions and subsequently integrates their trajectories numerically. This allows the dependent variable of the investigation—the fraction of systems that remain stable—to be determined statistically for each planetary multiplicity.

The central design principle of T.A.R.K.I.N. is the separation of **system generation**, **dynamical integration**, and **stability classification**. Separating these processes allows the same initial planetary architecture to be used to construct both a control system and a perturbed system. Consequently, differences in stability can be attributed to the presence of the external perturber rather than to an independently randomized set of planetary initial conditions.

For each value of planetary multiplicity,

$$
n \in \{2,3,4,5,6,7,8\}
$$

T.A.R.K.I.N. employs [REBOUND](https://rebound.readthedocs.io/), an N-body integrator that can integrate the motion of particles under the influence of gravity (Rein and Liu, 2012). REBOUND allows for high-volume repeated simulation that would be unfeasible to determine by hand.

T.A.R.K.I.N. generates an ensemble of initially stable planetary systems. Each generated system consists of a central star and $n$ planets whose initial orbital parameters are determined according to the predefined distributions described in the paper. Randomization is performed independently between systems while maintaining the same constraints across all values of $n$.

After generation, each system is divided into two corresponding experimental cases:

1. **Control system:** Contains only the central star and the $n$ planets.
2. **Perturbed system:** Contains the same star and planets but also includes an additional gravitational body.

Importantly, the perturbed and control systems originate from the same initial planetary configuration. This paired design reduces the influence of random variation between otherwise unrelated systems.

---

> **Project Status**
>
> This project is still very much under development and does not claim to make definitive scientific conclusions. As a student, I intend to learn and develop with time. The programming and scientific journey will be documented in this repository.
>
> This project is part of the International Baccalaureate Extended Essay (Physics).

---

# Critical Derivations

## Mutual Hill Radius (Determining Orbital Separation)
he Hill sphere framework and mutual Hill radii as a rule of
thumb measures how close two planets can get before their
gravity disrupts each other’s orbits (Gladman 1993). This project utilizes this value of the mutual Hill radius by effect of a spacing unit and mechanism. 

Let $a_i$ and $a_j$ denote the semi-major axes of two planets, where $a_j > a_i$. Here, $a_i$ represents the inner planet and $a_j$ the outer planet. Their orbital separation is defined as:

$$
\Delta a = a_j - a_i
$$

However, orbital separation alone does not account for the masses of the planets or their host star. To account for this, we define the mutual Hill radius:

$$
R_{\mathrm{H},ij}=
\frac{a_i + a_j}{2}
\left(
\frac{m_i + m_j}{3M_\star}
\right)^{1/3}
$$

The orbital separation can then be expressed as a dimensionless multiple of the mutual Hill radius. We define this spacing parameter as $\Delta$:

$$
\Delta = \frac{a_j - a_i}{R_{\mathrm{H},ij}}
$$

Rearranging gives:

$$
\Delta \frac{a_i + a_j}{2} \left(\frac{m_i + m_j}{3M_\star}\right)^{1/3}=
a_j - a_i
$$

For readability, let:

$$
k =
\Delta
\left(
\frac{m_i + m_j}{3M_\star}
\right)^{1/3}
$$

Substituting $k$ into the spacing equation gives:

$$
a_j - a_i = \frac{k}{2}(a_i + a_j)
$$

Expanding and rearranging to isolate $a_j$:

$$
\begin{aligned}
a_j - a_i &= \frac{k}{2}a_i + \frac{k}{2}a_j \\
a_j - \frac{k}{2}a_j &= a_i + \frac{k}{2}a_i \\
a_j\left(1-\frac{k}{2}\right)
&= a_i\left(1+\frac{k}{2}\right)
\end{aligned}
$$

Solving for the outer planet's semi-major axis yields:

$$
a_j =
a_i
\frac{1+\frac{k}{2}}{1-\frac{k}{2}}
$$

Substituting the definition of $k$ gives the final expression:

$$
a_j =
a_i
\frac{
1 + \dfrac{\Delta}{2}
\left(\dfrac{m_i+m_j}{3M_\star}\right)^{1/3}
}{
1 - \dfrac{\Delta}{2}
\left(\dfrac{m_i+m_j}{3M_\star}\right)^{1/3}
}
$$

This expression allows the outer planet's semi-major axis to be calculated from the inner planet's semi-major axis, the masses of both planets, the stellar mass, and the chosen mutual-Hill spacing.

For the resulting semi-major axis to be finite and positive, the denominator must be positive.

It is important to note that this spacing condition is applied during initialization. It does not represent the subsequent stability of the system throughout the integration, as that is precisely what this investigation seeks to evaluate.
