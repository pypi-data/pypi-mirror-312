import numpy as np
from .constellation import Constellation
from ._sig import Signal
from ..util.utils import moving_average


class Mod(Signal):
    def __init__(self, fs: int, message: np.ndarray | list, sps: int = 16, amplitude: float = 1, f: int = 100):
        """
        Class used for modulating data into a wave. Extends functionality from the Signal class by adding functions
        for doing various modulation operations.


        fs: Sampling frequency. How often samples will be created for the wave. A wave with a sampling rate of 100Hz
            would have 100 samples per second.
        message: A numpy array of ints containing the message symbols which will be written into a wave.
        sps: How many samples to generate per symbol. Typical values are between 8 and 20. Lowering the samples
            per symbol will increase the data rate at the expense of making it more susceptible to errors.
        amplitude: The (approximate) max amplitude of the wave, typically 1.
        f: The centre frequency of the signal. Should be somewhere between -fs/2 and fs/2.

        # Eg
        >>> s = Mod(20000, message=np.array([1, 0, 1, 1, 1, 2, 3]), sps=20, f=5000)    # instance a Signal object
        >>> (s.fs, s.message, s.sps, s.f)   # Display the parameters
        (20000, array([1, 0, 1, 1, 1, 2, 3]), 20, 5000)

        """
        super().__init__(fs=fs, message=message, sps=sps, amplitude=amplitude, f=f)

    def ASK(self) -> None:
        """
        Amplitude shift keying. Writes the message symbols into the amplitude of the wave by changing the A value in
        the equation:

            samples = A * e^i(*2pi*f*t + theta)

        Avoids zero amplitude symbols.

        # Example
        >>> s = Mod(10000, message=np.array([1, 0, 1, 1, 1]), sps=32, f=3000)
        >>> s.ASK()
        >>> s.samples   # test to see that the correct number of samples were actually made
        160
        """
        amp_mod_z = np.repeat(self.message, self.sps)       # repeat each of the element of the message, sps times
        amp_mod_z += 1  # Add 1 so amplitude is never 0 (I think this is necessary but it might not be)
        amp_mod_z = amp_mod_z / max(amp_mod_z)      # Scale it

        self.samples = self.create_samples(freq=self.f, amp=amp_mod_z)

    def create_FSK_vector(self, spacing: int) -> np.ndarray:
        """
        Creates the frequency shift keying vector which will be used by the FSK function to write data into a wave

        spacing: The Hz spacing of the FSK peaks. A bigger spacing makes it easier to seperate the symbols but spreads
        the signal across a bigger bandwidth.

        >>> s = Mod(10000, message=np.array([1, 0, 1, 1, 1]), sps=4, f=3000)    # Low FSK just for testing
        >>> FSK_vector = s.create_FSK_vector(spacing=200)
        >>> FSK_vector
        array([500, 500, 500, 500, 300, 300, 300, 300, 500, 500, 500, 500, 500,
        500, 500, 500, 500, 500, 500, 500])

        """
        freqs = self.message + 1      # Add one to avoid zero frequency
        freqs = freqs.astype(np.int64)  # self.message is np.uint8 so we have to change here to 64bit
        freqs = freqs * spacing

        # This centers it back on self.f, so that the centre frequency of the signal is maintained
        max_diff = abs((self.M)*spacing - self.f)
        min_diff = abs(spacing - self.f)
        change = int(abs(max_diff - min_diff)/2)

        if max_diff > min_diff:
            # We shift down
           freqs -= change
        elif min_diff > max_diff:
            # we shift up
            freqs += change

        # Stretch the vector so it lines up with the symbol transitions
        f_mod_z = np.repeat(freqs, self.sps)

        return f_mod_z

    def FSK(self, spacing: int) -> None:
        """
        Frequency shift keying. Writes the message symbols into the frequency of the wave by changing the f value in
        the equation:

            samples = A * e^i(*2pi*f*t + theta)

        frequency changes are additive with the centre frequency of the wave. Adds one to the centre frequency of the
        wave to avoid a zero frequency signal.

        spacing: The Hz spacing of the FSK peaks. A bigger spacing makes it easier to seperate the symbols but spreads
        the signal across a bigger bandwidth.

        >>> s = Mod(10000, message=np.array([1, 0, 1, 1, 1]), sps=32, f=3000)
        >>> s.FSK(spacing=300)  # 300hz between each peak
        >>> np.round(s.samples, 5).sum()    # Some test for reproducibility
        np.complex64(-0.7637102-3.7421002j)

        """
        f_mod_z = self.create_FSK_vector(spacing)

        z = self.create_samples(freq=f_mod_z, theta=0, amp=1)
        self.samples = z.astype(np.complex64)

    def QPSK(self):
        """
        Quadrature phase shift keying. This function writes data into the phase of the a wave by changing the theta
        parameter in the equation:

            samples = A * e^i(2pi*f*t + theta)

        Using QPSK will result in the symbols being mapped to the unit circle on the IQ graph.

        >>> m = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        >>> s = Mod(10000, message=m, sps=16, f=3000)
        >>> s.QPSK()  # 300hz between each peak
        >>> np.round(s.samples, 5).sum()  # Some test for reproducibility
        np.complex64(0.20153952+1.9175801j)

        """
        M = len(np.unique(self.message))    # The number of symbols

        # Convert the message symbols to M radian phase offsets with a pi/M bias from zero
        # i.e. if we had 4 symbols make them 45, 135, 225, 315 degree phase offsets (1/4pi, 3/4pi, 5/4pi, 7/4pi)
        symbols = self.message * 2 * np.pi / M + np.pi/ M
        message = np.repeat(symbols, self.sps)

        z = self.create_samples(freq=self.f, theta=message)

        self.samples = z.astype(np.complex64)

    def QAM(self, type="square", custom_map=None):
        """
        It's QAM! Creates the most ideal square QAM possible for the number of symbols supplied and the type
        """
        # Create the constellation map - a lookup table of values that will be indexed by the message values
        c = Constellation(M=self.M)

        if type == "square":
            c.square()
        elif type == "sunflower":
            c.sunflower()
        elif type == "star":
            c.star()
        elif type == "square_offset":
            c.square_offset()
        elif type == "custom":
            if custom_map is None:
                raise ValueError("Provide a custom constellation map in the custom_map argument")
            else:
                c.map = custom_map
        else:
            raise ValueError("Incorrect Constellation type")

        c.prune()
        c.normalise()

        message = np.repeat(self.message, self.sps)

        offsets = c.map[message]      # Index the map by the symbols

        z = self.create_samples(freq=self.f, theta=np.angle(offsets), amp=np.abs(offsets))

        self.samples = z

    def CPFSK(self, spacing):
        """
        samples = A * e^i(2pi*f*t + theta)

        Continuous phase frequency shift keying. Uses a phase offset vector to minimise phase jumps arising
        from frequency shift keying, which makes it more spectrally efficient.

        The squish factor squishes the frequencies together. The higher the squish the closer together they are.

        resource:
        https://dsp.stackexchange.com/questions/80768/fsk-modulation-with-python


        """
        # Create the frequency modulating vector
        f_mod_z = self.create_FSK_vector(spacing)

        # Cumulative phase offset
        delta_phi = 2.0 * f_mod_z * np.pi / self.fs    # Change in phase at every timestep (in radians per timestep)
        phi = np.cumsum(delta_phi)              # Add up the changes in phase

        z = self.amp * np.exp(1j * phi)  # creates sinusoid theta phase shift
        z = np.array(z)
        self.samples = z.astype(np.complex64)


    def CPFSK_smoother(self, spacing, smooth_n=10, weights=None):
        """
        samples = A * e^i(2pi*f*t + theta)

        Continuous phase frequency shift keying. Uses a phase offset vector to minimise phase jumps arising
        from frequency shift keying, which makes it more spectrally efficient.

        The squish factor squishes the frequencies together. The higher the squish the closer together they are.

        Smooth_n determines over how many samples the frequencies will be smoothed. This is how wide the moving average
        window is

        resource:
        https://dsp.stackexchange.com/questions/80768/fsk-modulation-with-python
        """
        # Create the frequency vector
        f_mod_z = self.create_FSK_vector(spacing)

        # Now we pass an averaging window over the frequencies. This will ensure we slowly transition from one
        # frequency to the next.

        # Test smooth_n argument
        if smooth_n <= 0:
            smooth_n = 1
        if smooth_n > self.sps:
            raise ValueError("smooth_n should not be greater than the samples per symbol")

        # Creating the smoothing window
        if weights is None:
            window = np.ones(smooth_n)
        else:
            window = np.array(weights)

        if smooth_n != len(window):
            raise ValueError("weights must have the same length as smooth_n")

        ma = moving_average(f_mod_z, smooth_n, weights=window)

        # Cumulative phase offset
        delta_phi = 2.0 * ma * np.pi / self.fs  # Change in phase at every timestep (in radians per timestep)
        phi = np.cumsum(delta_phi)  # Add up the changes in phase

        z = self.amp * np.exp(1j * phi)  # creates sinusoid theta phase shift
        z = np.array(z)
        self.samples = z.astype(np.complex64)

    def FHSS(self, hop_f, freqs, pattern=np.array([])):
        """
        Frequency hopping spread spectrum. Causes the signal to hop from frequency to frequency at a pre-define hop
        rate.
        """
        # If no pattern is given
        if len(pattern) == 0:
            pattern = np.arange(len(freqs))

        # The number of samples we transmit before hopping
        hop_samps = 1 / hop_f * self.fs

        # Make the FHSS vector
        f_mod_z = freqs[np.array(pattern)]
        f_mod_z = f_mod_z.repeat(hop_samps)
        n_tiles = int(np.ceil(len(self.samples) / len(f_mod_z)))
        # Repeat the pattern
        f_mod_z = np.tile(f_mod_z, n_tiles)
        # Trim it to fit
        f_mod_z = f_mod_z[0:len(self.samples)]

        # Now mod the wave with it
        angle = 2 * np.pi * f_mod_z * self.t
        z = np.cos(angle) + 1j * np.sin(angle)
        self.samples *= z[0:len(self.samples)]





