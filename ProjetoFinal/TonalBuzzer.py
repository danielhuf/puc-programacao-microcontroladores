from gpiozero import SourceMixin, CompositeDevice, PWMOutputDevice
import re
import warnings
from collections import namedtuple
try:
    from math import log2
except ImportError:
    from .compat import log2

class Tone(float):
    """
    Represents a frequency of sound in a variety of musical notations.

    :class:`Tone` class can be used with the :class:`~gpiozero.TonalBuzzer`
    class to easily represent musical tones. The class can be constructed in a
    variety of ways. For example as a straight frequency in `Hz`_ (which is the
    internal storage format), as an integer MIDI note, or as a string
    representation of a musical note.

    All the following constructors are equivalent ways to construct the typical
    tuning note, `concert A`_ at 440Hz, which is MIDI note #69:

        >>> from gpiozero.tones import Tone
        >>> Tone(440.0)
        >>> Tone(69)
        >>> Tone('A4')

    If you do not want the constructor to guess which format you are using
    (there is some ambiguity between frequencies and MIDI notes at the bottom
    end of the frequencies, from 128Hz down), you can use one of the explicit
    constructors, :meth:`from_frequency`, :meth:`from_midi`, or
    :meth:`from_note`, or you can specify a keyword argument when
    constructing::

        >>> Tone.from_frequency(440)
        >>> Tone.from_midi(69)
        >>> Tone.from_note('A4')
        >>> Tone(frequency=440)
        >>> Tone(midi=69)
        >>> Tone(note='A4')

    Several attributes are provided to permit conversion to any of the
    supported construction formats: :attr:`frequency`, :attr:`midi`, and
    :attr:`note`. Methods are provided to step :meth:`up` or :meth:`down` to
    adjacent MIDI notes.

    .. warning::

        Currently :class:`Tone` derives from :class:`float` and can be used as
        a floating point number in most circumstances (addition, subtraction,
        etc). This part of the API is not yet considered "stable"; i.e. we may
        decide to enhance / change this behaviour in future versions.

    .. _Hz: https://en.wikipedia.org/wiki/Hertz
    .. _concert A: https://en.wikipedia.org/wiki/Concert_pitch
    """

    tones = 'CCDDEFFGGAAB'
    semitones = {
        '♭': -1,
        'b': -1,
        '♮': 0,
        '':  0,
        '♯': 1,
        '#': 1,
    }
    regex = re.compile(
        r'(?P<note>[A-G])'
        r'(?P<semi>[%s]?)'
        r'(?P<octave>[0-9])' % ''.join(semitones.keys()))

    def __new__(cls, value=None, **kwargs):
        if value is None:
            if len(kwargs) != 1:
                raise TypeError('expected precisely one keyword argument')
            key, value = kwargs.popitem()
            try:
                return {
                    'frequency': cls.from_frequency,
                    'midi': cls.from_midi,
                    'note': cls.from_note,
                }[key](value)
            except KeyError:
                raise TypeError('unexpected keyword argument %r' % key)
        else:
            if kwargs:
                raise TypeError('cannot specify keywords with a value')
            if isinstance(value, (int, float)):
                if 0 <= value < 128:
                    if value > 0:
                        warnings.warn(
                            AmbiguousTone(
                                "Ambiguous tone specification; assuming you "
                                "want a MIDI note. To suppress this warning "
                                "use, e.g. Tone(midi=60), or to obtain a "
                                "frequency instead use, e.g. Tone(frequency="
                                "60)"))
                    return cls.from_midi(value)
                else:
                    return cls.from_frequency(value)
            elif isinstance(value, (bytes, str)):
                return cls.from_note(value)
            else:
                return cls.from_frequency(value)

    def __str__(self):
        return self.note

    def __repr__(self):
        try:
            midi = self.midi
        except ValueError:
            midi = ''
        else:
            midi = ' midi=%r' % midi
        try:
            note = self.note
        except ValueError:
            note = ''
        else:
            note = ' note=%r' % note
        return "<Tone%s%s frequency=%.2fHz>" % (note, midi, self.frequency)

    @classmethod
    def from_midi(cls, midi_note):
        """
        Construct a :class:`Tone` from a MIDI note, which must be an integer
        in the range 0 to 127. For reference, A4 (`concert A`_ typically used
        for tuning) is MIDI note #69.

        .. _concert A: https://en.wikipedia.org/wiki/Concert_pitch
        """
        midi = int(midi_note)
        if 0 <= midi_note < 128:
            A4_midi = 69
            A4_freq = 440
            return cls.from_frequency(A4_freq * 2 ** ((midi - A4_midi) / 12))
        raise ValueError('invalid MIDI note: %r' % midi)


    @classmethod
    def from_note(cls, note):
        """
        Construct a :class:`Tone` from a musical note which must consist of
        a capital letter A through G, followed by an optional semi-tone
        modifier ("b" for flat, "#" for sharp, or their Unicode equivalents),
        followed by an octave number (0 through 9).

        For example `concert A`_, the typical tuning note at 440Hz, would be
        represented as "A4". One semi-tone above this would be "A#4" or
        alternatively "Bb4". Unicode representations of sharp and flat are also
        accepted.
        """
        if isinstance(note, bytes):
            note = note.decode('ascii')
        if isinstance(note, str):
            match = Tone.regex.match(note)
            if match:
                octave = int(match.group('octave')) + 1
                return cls.from_midi(
                    Tone.tones.index(match.group('note')) +
                    Tone.semitones[match.group('semi')] +
                    octave * 12)
        raise ValueError('invalid note specification: %r' % note)


    @classmethod
    def from_frequency(cls, freq):
        """
        Construct a :class:`Tone` from a frequency specified in `Hz`_ which
        must be a positive floating-point value in the range 0 < freq <= 20000.

        .. _Hz: https://en.wikipedia.org/wiki/Hertz
        """
        if 0 < freq <= 20000:
            return super(Tone, cls).__new__(cls, freq)
        raise ValueError('invalid frequency: %.2f' % freq)


    @property
    def frequency(self):
        """
        Return the frequency of the tone in `Hz`_.

        .. _Hz: https://en.wikipedia.org/wiki/Hertz
        """
        return float(self)

    @property
    def midi(self):
        """
        Return the (nearest) MIDI note to the tone's frequency. This will be an
        integer number in the range 0 to 127. If the frequency is outside the
        range represented by MIDI notes (which is approximately 8Hz to 12.5KHz)
        :exc:`ValueError` exception will be raised.
        """
        result = int(round(12 * log2(self.frequency / 440) + 69))
        if 0 <= result < 128:
            return result
        raise ValueError('%f is outside the MIDI note range' % self.frequency)

    @property
    def note(self):
        """
        Return the (nearest) note to the tone's frequency. This will be a
        string in the form accepted by :meth:`from_note`. If the frequency is
        outside the range represented by this format ("A0" is approximately
        27.5Hz, and "G9" is approximately 12.5Khz) a :exc:`ValueError`
        exception will be raised.
        """
        offset = self.midi - 60  # self.midi - A4_midi + Tone.tones.index('A')
        index = offset % 12      # offset % len(Tone.tones)
        octave = 4 + offset // 12
        if 0 <= octave <= 9:
            return (
                Tone.tones[index] +
                ('#' if Tone.tones[index] == Tone.tones[index - 1] else '') +
                str(octave)
            )
        raise ValueError('%f is outside the notation range' % self.frequency)

    def up(self, n=1):
        """
        Return the :class:`Tone` *n* semi-tones above this frequency (*n*
        defaults to 1).
        """
        return Tone.from_midi(self.midi + n)


    def down(self, n=1):
        """
        Return the :class:`Tone` *n* semi-tones below this frequency (*n*
        defaults to 1).
        """
        return Tone.from_midi(self.midi - n)

class TonalBuzzer(SourceMixin, CompositeDevice):
    """
    Extends :class:`CompositeDevice` and represents a tonal buzzer.

    :type pin: int or str
    :param pin:
        The GPIO pin which the buzzer is connected to. See :ref:`pin-numbering`
        for valid pin numbers. If this is :data:`None` a :exc:`GPIODeviceError`
        will be raised.

    :param float initial_value:
        If :data:`None` (the default), the buzzer will be off initially. Values
        between -1 and 1 can be specified as an initial value for the buzzer.

    :type mid_tone: int or str
    :param mid_tone:
        The tone which is represented the device's middle value (0). The
        default is "A4" (MIDI note 69).

    :param int octaves:
        The number of octaves to allow away from the base note. The default is
        1, meaning a value of -1 goes one octave below the base note, and one
        above, i.e. from A3 to A5 with the default base note of A4.

    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).

    .. note::

        Note that this class does not currently work with
        :class:`~gpiozero.pins.pigpio.PiGPIOFactory`.
    """

    def __init__(self, pin=None, initial_value=None, mid_tone=Tone("A4"),
                 octaves=1, pin_factory=None):
        self._mid_tone = None
        super(TonalBuzzer, self).__init__(
            pwm_device=PWMOutputDevice(
                pin=pin, pin_factory=pin_factory
            ), pin_factory=pin_factory)
        try:
            self._mid_tone = Tone(mid_tone)
            if not (0 < octaves <= 9):
                raise ValueError('octaves must be between 1 and 9')
            self._octaves = octaves
            try:
                self.min_tone.note
            except ValueError:
                raise ValueError(
                    '%r is too low for %d octaves' %
                    (self._mid_tone, self._octaves))
            try:
                self.max_tone.note
            except ValueError:
                raise ValueError(
                    '%r is too high for %d octaves' %
                    (self._mid_tone, self._octaves))
            self.value = initial_value
        except:
            self.close()
            raise

    def __repr__(self):
        try:
            self._check_open()
            if self.value is None:
                return '<gpiozero.TonalBuzzer object on pin %r, silent>' % (
                    self.pwm_device.pin,)
            else:
                return '<gpiozero.TonalBuzzer object on pin %r, playing %s>' % (
                    self.pwm_device.pin, self.tone.note)
        except DeviceClosed:
            return super(TonalBuzzer, self).__repr__()

    def play(self, tone):
        """
        Play the given *tone*. This can either be an instance of
        :class:`~gpiozero.tones.Tone` or can be anything that could be used to
        construct an instance of :class:`~gpiozero.tones.Tone`.

        For example::

            >>> from gpiozero import TonalBuzzer
            >>> from gpiozero.tones import Tone
            >>> b = TonalBuzzer(17)
            >>> b.play(Tone("A4"))
            >>> b.play(Tone(220.0)) # Hz
            >>> b.play(Tone(60)) # middle C in MIDI notation
            >>> b.play("A4")
            >>> b.play(220.0)
            >>> b.play(60)
        """
        if tone is None:
            self.value = None
        else:
            if not isinstance(tone, Tone):
                tone = Tone(tone)
            freq = tone.frequency
            if self.min_tone.frequency <= tone <= self.max_tone.frequency:
                self.pwm_device.pin.frequency = freq
                self.pwm_device.value = 0.5
            else:
                raise ValueError("tone is out of the device's range")


    def stop(self):
        """
        Turn the buzzer off. This is equivalent to setting :attr:`value` to
        :data:`None`.
        """
        self.value = None


    @property
    def tone(self):
        """
        Returns the :class:`~gpiozero.tones.Tone` that the buzzer is currently
        playing, or :data:`None` if the buzzer is silent. This property can
        also be set to play the specified tone.
        """
        if self.pwm_device.pin.frequency is None:
            return None
        else:
            return Tone.from_frequency(self.pwm_device.pin.frequency)

    @tone.setter
    def tone(self, value):
        self.play(value)

    @property
    def value(self):
        """
        Represents the state of the buzzer as a value between -1 (representing
        the minimum tone) and 1 (representing the maximum tone). This can also
        be the special value :data:`None` indicating that the buzzer is
        currently silent.
        """
        if self.pwm_device.pin.frequency is None:
            return None
        else:
            # Can't have zero-division here; zero-frequency Tone cannot be
            # generated and self.octaves cannot be zero either
            return log2(
                self.pwm_device.pin.frequency / self.mid_tone.frequency
            ) / self.octaves

    @value.setter
    def value(self, value):
        if value is None:
            self.pwm_device.pin.frequency = None
        elif -1 <= value <= 1:
            freq = self.mid_tone.frequency * 2 ** (self.octaves * value)
            self.pwm_device.pin.frequency = freq
            self.pwm_device.value = 0.5
        else:
            raise OutputDeviceBadValue(
                'TonalBuzzer value must be between -1 and 1, or None')

    @property
    def is_active(self):
        """
        Returns :data:`True` if the buzzer is currently playing, otherwise
        :data:`False`.
        """
        return self.value is not None

    @property
    def octaves(self):
        """
        The number of octaves available (above and below mid_tone).
        """
        return self._octaves

    @property
    def min_tone(self):
        """
        The lowest tone that the buzzer can play, i.e. the tone played
        when :attr:`value` is -1.
        """
        return self._mid_tone.down(12 * self.octaves)

    @property
    def mid_tone(self):
        """
        The middle tone available, i.e. the tone played when :attr:`value` is
        0.
        """
        return self._mid_tone

    @property
    def max_tone(self):
        """
        The highest tone that the buzzer can play, i.e. the tone played when
        :attr:`value` is 1.
        """
        return self._mid_tone.up(12 * self.octaves)