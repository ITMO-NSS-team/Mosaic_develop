# Multipliers for resizing of inserting parts of images
MIN_MULTIPLIER: float = 0.3
MAX_MULTIPLIER: float = 2
# Deltas for creating small area around objects(in pixels)
DELTA_X: int = 2
DELTA_Y: int = 2
# Maximum images in mosaic
MAX_IMAGES: int = 30
# Formats for output mosaics
IMAGES_FORMAT: str = ".jpg"
ANNOTATIONS_FORMAT: str = ".txt"
# Minimum size of areas relatively to main image (0-1)
AREA_SIZE = 0.2
# Divider for creating areas with objects
DIVIDER = 4
# Number of attempts to get empty part of main image
ATTEMPTS_FOR_GET_EMPTY_PART_OF_IMAGE = 15
# Number of attempts to get part of image with object
ATTEMPTS_FOR_GET_IMAGE_WITH_OBJECT = 25
# Formats for output files
IMAGE_FORMAT = ".jpg"
ANNOTATION_FORMAT = ".txt"