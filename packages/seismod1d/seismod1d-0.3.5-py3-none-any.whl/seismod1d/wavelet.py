import numpy as np
from scipy import signal
from collections import namedtuple


def get_wavelet(
    wav_duration=0.2,
    wav_dt=0.004,
    wav_type="ricker",
    wav_parameters={"wav_ricker_freq": 30},
):

    # - initiate output
    wav_time = np.nan
    wav_amplitude = np.nan

    # get wavelet based on type
    if wav_type == "ricker":

        # - assign input parameters
        wav_ricker_freq = wav_parameters["wav_ricker_freq"]

        # - get wavelet in time domain
        ww = _ricker(wav_duration, wav_dt, wav_ricker_freq)
        wav_time = ww.time  # wavelet time
        wav_amplitude = ww.amplitude  # wavelet amplitude

        # - make string
        wav_name = "Ricker (" + str(wav_ricker_freq) + " Hz)"

    elif wav_type == "ormsby":

        # - assign input parameters
        wav_ormsby_freq = wav_parameters["wav_ormsby_freq"]

        # - get wavelet in time domain
        ww = _ormsby(wav_duration, wav_dt, wav_ormsby_freq)
        wav_time = ww.time  # wavelet time
        wav_amplitude = ww.amplitude  # wavelet amplitude

        # - make string
        ss = "".join([str(ff) + "-" for ff in wav_ormsby_freq])
        wav_name = "Ormsby (" + ss[:-1] + " Hz)"

        # - apply hanning filter
        hann_filter = signal.windows.hann(len(wav_time) + 1)
        wav_amplitude = wav_amplitude * hann_filter[:-1]

    # return wavelet in time domain
    return wav_time, wav_amplitude, wav_name


def time_to_frequency(wav_time, wav_amplitude, crop_positive=False):

    # Obtain frequency power spectrum from wavelet in time

    # - time vector
    tv = wav_time
    dt = tv[1] - tv[0]
    ntv = len(tv)

    # - define frequency vector for FFT
    nf = int(pow(2, np.ceil(np.log(ntv) / np.log(2))))
    df = 1 / (dt * nf)
    # frequency sampling
    fmin = -0.5 * df * nf
    fv = fmin + df * np.arange(0, nf)  # frequency vector

    # - wavelet in f-domain
    ww_ap = np.zeros(nf)  # initilize wavelet amplitude padded with zeros
    ww_ap[: len(wav_amplitude)] = wav_amplitude  # insert wavelet amplitude
    ww_af = np.fft.fft(ww_ap)  # wavelet in frequency domain
    ww_af = np.fft.fftshift(ww_af)

    # - crop freq vector and normalize power spectrum
    if crop_positive:
        ww_af = ww_af[fv >= 0]
        wav_frequency = fv[fv >= 0]
        wav_spectrum = np.abs(ww_af) / max(np.abs(ww_af))

    # - return
    return wav_frequency, wav_spectrum

def _get_time(duration, dt):
    """
    Make a time vector.

    The time vector will have an odd number of samples,
    and will be symmetric about 0.
    """
    # This business is to avoid some of the issues with `np.arange`:
    # (1) unpredictable length and (2) floating point weirdness, like
    # 1.234e-17 instead of 0. Not using `linspace` because figuring out
    # the length and offset gave me even more of a headache than this.
    n = int(duration / dt)
    odd = n % 2
    k = int(10**-np.floor(np.log10(dt)))
    dti = int(k * dt)  # integer dt

    if (odd):
        t = np.arange(n)
    elif (not odd):
        t = np.arange(n + 1)

    t -= t[-1] // 2

    return dti * t / k

def _ricker(duration, dt, f):
    """
    Also known as the mexican hat wavelet, models the function:

    .. math::
        A =  (1 - 2 \pi^2 f^2 t^2) e^{-\pi^2 f^2 t^2}

    .. plot::

        import matplotlib.pyplot as plt
        w, t = _ricker(0.256, 0.002, 40)
        plt.plot(t, w)

    Args:
        duration (float): The length in seconds of the wavelet.
        dt (float): The sample interval in seconds (often one of  0.001, 0.002,
            or 0.004).
        f (float): Centre frequency of the wavelet in Hz.

    Returns:
        ndarray: A vector containing a tuple of (wavelet, t) is returned.

    """
    t = _get_time(duration, dt)
    
    pft2 = (np.pi * f * t) ** 2
    w = np.squeeze((1 - (2 * pft2)) * np.exp(-pft2))

    RickerWavelet = namedtuple("RickerWavelet", ["amplitude", "time"])
    return RickerWavelet(w, t)


def _ormsby(duration, dt, f):
    """
    The Ormsby wavelet requires four frequencies which together define a
    trapezoid shape in the spectrum. The Ormsby wavelet has several sidelobes,
    unlike Ricker wavelets.

    .. plot::

        import matplotlib.pyplot as plt
        w, t = _ormsby(0.256, 0.002, [5, 10, 40, 80])
        plt.plot(t, w)

    Args:
        duration (float): The length in seconds of the wavelet.
        dt (float): The sample interval in seconds (usually 0.001, 0.002,
            or 0.004).
        f (array-like): A tuple of frequencies (f1, f2, f3, f4).
    Returns:
        ndarray: A vector containing a tuple of (wavelet, t) is returned.

    """
    try:
        f = np.array(f).reshape(4)
    except ValueError:
        raise ValueError("The dimension of the frequency array must be of size 4.")

    t = _get_time(duration, dt)
    f1, f2, f3, f4 = f

    def numerator(f, t):
        """The numerator in the Ormsby equation."""
        return (np.sinc(f * t) ** 2) * ((np.pi * f) ** 2)

    pf43 = (np.pi * f4) - (np.pi * f3)
    pf21 = (np.pi * f2) - (np.pi * f1)

    w = (
        (numerator(f4, t) / pf43)
        - (numerator(f3, t) / pf43)
        - (numerator(f2, t) / pf21)
        + (numerator(f1, t) / pf21)
    )

    OrmsbyWavelet = namedtuple("OrmsbyWavelet", ["amplitude", "time"])
    return OrmsbyWavelet(np.squeeze(w) / np.amax(w), t)
