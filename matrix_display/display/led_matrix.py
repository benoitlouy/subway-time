from rgbmatrix import RGBMatrix, RGBMatrixOptions

class Display:
    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.parallel = 1
        options.hardware_mapping = 'regular'
        self.matrix = RGBMatrix(options = options)

    def refresh(self, image):
        self.matrix.SetImage(image.convert('RGB'))
