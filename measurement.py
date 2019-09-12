class Measurement():
    DATA_LENGTH = 32
    FRAME_LENGTH = 28
    START_BYTES = '42 4D'
    DATA_INDEX = slice(4, 28)
    LENGTH_INDEX = slice(2, 4) 
    HIGH_BIT_INDEX = slice(0, None, 2)

    COLUMNS = [
        "PM 1.0 CF1",
        "PM 2.5 CF1",
        "PM 10 CF1",
        "PM 1.0 Atmosphere",
        "PM 2.5 Atmosphere",
        "PM 10 Atmosphere",
        "PM 0.3 Count",
        "PM 0.5 Count",
        "PM 1.0 Count",
        "PM 2.5 Count",
        "PM 5.0 Count",
        "PM 10 Count"
    ]

    def __init__(self, raw_bytes):
        self.raw_bytes = raw_bytes
        self.data = Measurement.parse(raw_bytes)

    @staticmethod
    def check_start_bytes(message):
        expected = bytes.fromhex(Measurement.START_BYTES)
        if message.startswith(expected) is not True:
            raise ValueError('Start bytes are not well formed')

    @staticmethod
    def check_length(message):
        length_bytes = message[Measurement.LENGTH_INDEX]
        length = (length_bytes[0] << 8) + length_bytes[1]
        if length != Measurement.FRAME_LENGTH:
            raise ValueError('Unexpected frame length')

    @staticmethod
    def parse(message):
        try:
            Measurement.check_start_bytes(message)
            Measurement.check_length(message)
            # Convert byte array to list of ints
            data = list(message[Measurement.DATA_INDEX])
            # Interpret ints as pairs of bytes
            data[Measurement.HIGH_BIT_INDEX] = \
                map(lambda x: x << 8, data[Measurement.HIGH_BIT_INDEX]) 
            # Combine high order and lower order bytes
            pairs = zip(data[0::2], data[1::2])
            values = map(lambda x: x[0] + x[1], pairs) 

            return list(values)

        except ValueError:
            pass

    def __str__(self):
        return str(self.data)
