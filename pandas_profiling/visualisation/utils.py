from typing import Union, Tuple
import base64
from io import BytesIO
from urllib.parse import quote

from pandas_profiling.config import config


def hex_to_rgb(hex: str) -> Tuple[float, ...]:
    """Format a hex value (#FFFFFF) as normalized RGB (1.0, 1.0, 1.0).

    Args:
        hex: The hex value.

    Returns:
        The RGB representation of that hex color value.
    """
    hex = hex.lstrip("#")
    hlen = len(hex)
    return tuple(
        int(hex[i : i + hlen // 3], 16) / 255 for i in range(0, hlen, hlen // 3)
    )


def plot_360_n0sc0pe(plt, image_format: Union[str, None] = None, attempts=0) -> str:
    """Quickscope the plot to a base64 encoded string.

    Args:
        image_format: png or svg, overrides config.
        plt: The pyplot module.
        attempts: number to tries

    Returns:
        A base64 encoded version of the plot in the specified image format.
    """
    if image_format is None:
        image_format = config["plot"]["image_format"].get(str)
    dpi = config["plot"]["dpi"].get(int)

    if image_format not in ["svg", "png"]:
        raise ValueError('Can only 360 n0sc0pe "png" or "svg" format.')

    mime_types = {"png": "image/png", "svg": "image/svg+xml"}

    try:
        image_data = BytesIO()
        plt.savefig(image_data, dpi=dpi, format=image_format)
        image_data.seek(0)
        result_string = "data:{mime_type};base64,{image_data}".format(
            mime_type=mime_types[image_format],
            image_data=quote(base64.b64encode(image_data.getvalue())),
        )
        plt.close()
    except RuntimeError:
        plt.close()
        # Hack https://stackoverflow.com/questions/44666207/matplotlib-error-when-running-plotting-in-multiprocess
        # #comment79373127_44666207
        if attempts > 10:
            return ""
        else:
            return plot_360_n0sc0pe(plt, image_format, attempts + 1)
    finally:
        plt.close("all")

    return result_string
