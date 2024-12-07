from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from yta_general_utils.math import Math
from yta_general_utils.random import random_int_between
from yta_multimedia.image.edition.resize import resize_image
from yta_multimedia.video.edition.resize import resize_video
from yta_multimedia.video.parser import VideoParser
from PIL import Image
from typing import Union

import numpy as np


# TODO: All this is related to Image so multimedia (?)
class PixelFilterFunction:
    """
    Class to interact with image pixels and detect greens or transparent
    pixels to be used in, for example, ImageRegionFinder functionality.
    """
    @staticmethod
    def is_green(pixel):
        """
        This filter is the one we use to make sure it is a greenscreen
        color part by applying a [[0, r, 100], [100, g, 255], [0, b, 100]]
        filtering.
        """
        r, g, b = pixel

        return (r >= 0 and r <= 100) and (g >= 100 and g <= 255) and (b >= 0 and b <= 100)
    
    @staticmethod
    def is_transparent(pixel):
        """
        Checks if the alpha channel (4th in array) is set to 0 (transparent).
        The pixel must be obtained from a RGBA image (so 4 dimentions
        available).
        """
        _, _, _, a = pixel

        return a == 0
    
NORMALIZATION_MIN_VALUE = -10000
NORMALIZATION_MAX_VALUE = 10000

class CoordinateType(Enum):
    """
    Enum class to represent a coordinate type that 
    defines the way to make the calculations.
    """
    CORNER = 'corner'
    """
    The type of coordinate that represents the upper
    left corner of the object that uses the coordinate
    with this type.
    """
    CENTER = 'center'
    """
    The type of coordinate that represents the center of
    the object that uses the coordinate with this type.
    """

class Coordinate:
    """
    Class to represent a coordinate point ('x', 'y').
    """
    position: tuple = None
    """
    The ('x', 'y') tuple containing the position
    coordinate.
    """
    _is_normalized: bool = False
    """
    Internal function to know if it has been normalized
    or not.
    """

    @property
    def x(self):
        return self.position[0]
    
    @property
    def y(self):
        return self.position[1]
    
    @property
    def is_normalized(self):
        return self._is_normalized

    def __init__(self, x: float, y: float, is_normalized: bool = False):
        if not NumberValidator.is_number_between(x, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE) or not NumberValidator.is_number_between(y, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE):
            raise Exception(f'The "x" and "y" parameters must be values between {str(NORMALIZATION_MIN_VALUE)} and {str(NORMALIZATION_MAX_VALUE)} and "{str(x)}, {str(y)}" provided.')
        
        if not PythonValidator.is_boolean(is_normalized):
            raise Exception('The "is_normalized" parameter must be a boolean value.')
        
        self.position = (x, y)
        self._is_normalized = is_normalized

    def get_x(self):
        """
        Return the 'x' value.
        """
        return self.x
    
    def get_y(self):
        """
        Return the 'y' value.
        """
        return self.y

    def as_tuple(self):
        """
        Return the coordinate as a tuple ('x', 'y').
        """
        return Coordinate.to_tuple(self)
    
    def as_array(self):
        """
        Return the coordinate as an array ['x', 'y'].
        """
        return Coordinate.to_array(self)

    def normalize(self):
        """
        Normalize the coordinate by turning the values into
        a range between [0.0, 1.0]. This will be done if the
        values have not been normalized previously.
        """
        if not self._is_normalized:
            self.position = Coordinate.normalize_tuple(self.position)
            self._is_normalized = True

        return self

    def denormalize(self):
        """
        Denormalize the coordinate values by turning them
        from normalized values to the real ones. This will
        be done if the values have been normalized 
        previously.
        """
        if self._is_normalized:
            self.position = Coordinate.denormalize_tuple(self.position)
            self._is_normalized = False

        return self

    @staticmethod
    def to_tuple(coordinate):
        """
        Turn the provided 'coordinate' to a tuple like ('x', 'y').
        """
        return coordinate.position
    
    @staticmethod
    def to_array(coordinate):
        """
        Turn the provided 'coordinate' to an array like ['x', 'y'].
        """
        return [coordinate.x, coordinate.y]

    @staticmethod
    def generate(amount: int = 1):
        """
        Generate 'amount' coordinates with random values
        between [0, 1920] for the 'x' and [0, 1080] for
        the 'y', that are returned as an array of instances.

        The 'amount' parameter is limited to the interval 
        [1, 100].
        """
        if not NumberValidator.is_number_between(amount, 1, 100):
            raise Exception(f'The provided "amount" parameter "{str(amount)}" is not a number between 1 and 100.')
        
        return Coordinate(random_int_between(0, 1920), random_int_between(0, 1080))
    
    @staticmethod
    def to_numpy(coordinates: list['Coordinate']):
        """
        Convert a list of Coordinates 'coordinates' to
        numpy array to be able to work with them.

        This method does the next operation:
        np.array([[coord.x, coord.y] for coord in coordinates])
        """
        if not PythonValidator.is_list(coordinates):
            if not PythonValidator.is_instance(coordinates, Coordinate):
                raise Exception('The provided "coordinates" parameter is not a list of NormalizedCoordinates nor a single NormalizedCoordinate instance.')
            else:
                coordinates = [coordinates]
        elif any(not PythonValidator.is_instance(coordinate, Coordinate) for coordinate in coordinates):
            raise Exception('At least one of the provided "coordinates" is not a NormalizedCoordinate instance.')

        return np.array([coordinate.as_array() for coordinate in coordinates])
    
    @staticmethod
    def normalize_tuple(coordinate: tuple):
        """
        Normalize the provided 'coordinate' by applying
        our normalization limits. This means turning the
        non-normalized 'coordinate' to a normalized one
        (values between 0.0 and 1.0).
        """
        return (
            Math.normalize(coordinate[0], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE),
            Math.normalize(coordinate[1], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)
        )
    
    @staticmethod
    def denormalize_tuple(coordinate: tuple):
        """
        Denormalize the provided 'coordinate' by applying
        our normalization limits. This means turning the 
        normalized 'coordinate' (values between 0.0 and
        1.0) to the not-normalized ones according to our
        normalization limits.
        """
        return (
            Math.denormalize(coordinate[0], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE),
            Math.denormalize(coordinate[1], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)
        )
    
    @staticmethod
    def is_valid(coordinate: tuple):
        """
        Check if the provided 'coordinate' is valid or not.
        A valid coordinate is a tuple with two elements that
        are values between our normalization limits.
        """
        if not PythonValidator.is_instance(coordinate, 'Coordinate') and (not PythonValidator.is_tuple(coordinate) or len(coordinate) != 2 or not NumberValidator.is_number_between(coordinate[0], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE) or not NumberValidator.is_number_between(coordinate[1], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)):
            return False
        
        return True

    @staticmethod
    def validate(coordinate: tuple, parameter_name: str):
        """
        Validate if the provided 'coordinate' is a coordinate
        with values between our normalization limits.
        """
        if not Coordinate.is_valid(coordinate):
            raise Exception(f'The provided "{parameter_name}" parameter is not a valid tuple of 2 elements that are values between our limits {str(NORMALIZATION_MIN_VALUE)} and {str(NORMALIZATION_MAX_VALUE)}. Please, provide a valid coordinate.')

class Region:
    """
    Class to represent a region built by two coordinates, one in
    the top left corner and another one in the bottom right 
    corner.
    """
    top_left: Coordinate = None
    bottom_right: Coordinate = None
    _width: int = None
    _height: int = None

    def __init__(self, top_left_x: int, top_left_y: int, bottom_right_x: int, bottom_right_y: int):
        self.top_left = Coordinate(top_left_x, top_left_y)
        self.bottom_right = Coordinate(bottom_right_x, bottom_right_y)
        self._width = self.bottom_right.get_x() - self.top_left.get_x()
        self._height = self.bottom_right.get_y() - self.top_left.get_y()

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    def resize_image_to_fit_in(self, image):
        """
        This method rescales the provided 'image' to make it fit in
        this region. Once it's been rescaled, this image should be
        placed in the center of the region.
        """
        image = ImageParser.to_pillow(image)

        image = resize_image(image, (self.width, self.height))

        # We enlarge it by a 1% to avoid some balck pixels lines
        image = image.resize((image.size[0] * 1.01, image.size[1] * 1.01))

        return image

    # TODO: This could be private maybe
    # TODO: I should do this in yta_multimedia as it is
    # video related
    def resize_video_to_fit_in(self, video):
        """
        This method rescales the provided 'video' to make it fit in
        this region. Once it's been rescaled, this video should be
        placed in the center of the region.
        """
        video = VideoParser.to_moviepy(video)

        video = resize_video(video, (self.width, self.height))

        # We enlarge it by a 1% to avoid some black pixels lines
        video = video.resize(1.01)

        return video
    
    def place_video_inside(self, video):
        """
        This method rescales the provided 'video' to make it fit in
        this region. Once it's been rescaled, this videos is 
        positioned in the required position to fit the region.
        """
        video = self.resize_video_to_fit_in(video)

        x = (self.bottom_right.x + self.top_left.x) / 2 - video.w / 2
        y = (self.bottom_right.y + self.top_left.y) / 2 - video.h / 2

        # TODO: What about upper limits (out of bottom left bounds) (?)
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        video = video.set_position((x, y))

        return video

class ImageRegionFinder:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    @classmethod
    def is_valid(cls, x, y, image, visited, filter_func: callable):
        """
        This method verifies if the pixel is between the limits
        and is transparent and unvisited.
        """
        rows, cols, _ = image.shape

        return (0 <= x < rows and 0 <= y < cols and not visited[x, y] and filter_func(image[x, y]))

    @classmethod
    def dfs(cls, image: np.ndarray, visited, x, y, region, filter_func: callable):
        """
        A Deep First Search algorithm applied to the image to 
        obtain all the pixels connected in a region.
        """
        if not isinstance(image, np.ndarray):
            raise Exception('The provided "image" parameter is not a valid np.ndarray.')

        stack = [(x, y)]
        visited[x, y] = True
        region.append((x, y))
        
        while stack:
            cx, cy = stack.pop()
            for dx, dy in cls.directions:
                nx, ny = cx + dx, cy + dy
                if cls.is_valid(nx, ny, image, visited, filter_func):
                    visited[nx, ny] = True
                    region.append((nx, ny))
                    stack.append((nx, ny))

    @classmethod
    def is_inside(cls, small_bounds, large_bounds):
        """
        This method verifies if the bounds of a found region are
        inside another bounds to discard the smaller regions.
        """
        min_x_small, max_x_small, min_y_small, max_y_small = small_bounds
        min_x_large, max_x_large, min_y_large, max_y_large = large_bounds
        
        return (
            min_x_small >= min_x_large and max_x_small <= max_x_large and
            min_y_small >= min_y_large and max_y_small <= max_y_large
        )

    @classmethod
    def find_regions(cls, image: np.ndarray, filter_func: PixelFilterFunction) -> list[Region]:
        """
        This method looks for all the existing regions of transparent
        pixels that are connected ones to the others (neighbours). The
        'filter_func' parameter is the one that will classify the pixels
        as, for example, transparent or green. That 'filter_func' must
        be a method contained in the PixelFilterFunction class.

        This method returns the found regions as objects with 'top_left'
        and 'bottom_right' fields that are arrays of [x, y] positions
        corresponding to the corners of the found regions.
        """
        if not isinstance(image, np.ndarray):
            raise Exception('The provided "image" parameter is not a valid np.ndarray.')

        rows, cols, _ = image.shape
        visited = np.zeros((rows, cols), dtype=bool)
        regions = []
        
        for row in range(rows):
            for col in range(cols):
                # If we find a transparent pixel, we search
                if filter_func(image[row, col]) and not visited[row, col]:
                    region = []
                    cls.dfs(image, visited, row, col, region, filter_func)
                    
                    if region:
                        min_x = min(px[0] for px in region)
                        max_x = max(px[0] for px in region)
                        min_y = min(px[1] for px in region)
                        max_y = max(px[1] for px in region)
                        
                        # These are the limits of the region
                        bounds = (min_x, max_x, min_y, max_y)
                        
                        # We need to avoid small regions contained in others
                        if not any(cls.is_inside(bounds, r['bounds']) for r in regions):
                            regions.append({
                                # TODO: Maybe we need them to turn into transparent pixels
                                #'coordinates': region, # We don't need coordinates
                                'bounds': bounds
                            })

        # I want another format, so:
        for index, region in enumerate(regions):
            regions[index] = Region(region['bounds'][2], region['bounds'][0], region['bounds'][3], region['bounds'][1])
            # regions[index] = {
            #     # 'top_left': [region['bounds'][0], region['bounds'][2]],
            #     # 'bottom_right': [region['bounds'][1], region['bounds'][3]]
            #     # I don't know why I have to use it in this order but...
            #     'top_left': [region['bounds'][2], region['bounds'][0]],
            #     'bottom_right': [region['bounds'][3], region['bounds'][1]]
            # }

        return regions
    
    @classmethod
    def find_green_regions(cls, image: Union[str, Image.Image, np.ndarray]) -> list[Region]:
        """
        This method returns the found green regions as objects with
        'top_left' and 'bottom_right' fields that are arrays of [x, y] 
        positions corresponding to the corners of the found regions.
        """
        image = ImageParser.to_numpy(image, 'RGB')
            
        return cls.find_regions(image, PixelFilterFunction.is_green)
    
    @classmethod
    def find_transparent_regions(cls, image: Union[str, Image.Image, np.ndarray]) -> list[Region]:
        """
        This method returns the found transparent regions as objects
        with 'top_left' and 'bottom_right' fields that are arrays of
        [x, y] positions corresponding to the corners of the found
        regions.
        """
        image = ImageParser.to_numpy(image, 'RGBA')
            
        return cls.find_regions(image, PixelFilterFunction.is_transparent)