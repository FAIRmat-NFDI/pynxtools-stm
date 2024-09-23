from pySPM.Bruker import Bruker
import contextlib
import pySPM

import re
from typing import Any

__all__ = ["BrukerSPM"]


class BrukerSPM(Bruker):
    # TODO: Recheck the functionality of the
    __all__ = ["list_channels", "get_channel_data", "get_channel_image"]

    def __init__(self, path):
        self.path = path
        # After with the parent pat the leaf key will be added.
        parent_key = ""
        # Last part of the administrative path
        last_admin_key_order = ["", 0]
        got_leaf_key = False
        # Includes also all the metadata
        # TODO: rename the parse_data to metadata
        self.parsed_data: dict[str, Any] = {}
        with open(self.path, "rb") as file:
            self.layers = []
            self.scanners = []
            mode = ""
            while True:
                line = file.readline().rstrip().replace(b"\\", b"")
                if line == b"*Ciao image list":
                    self.layers.append({})
                    mode = "Image"
                elif line == b"*Scanner list":
                    self.scanners.append({})
                    mode = "Scanner"
                elif line.startswith(b"*EC"):
                    mode = "EC"
                else:
                    args = line.split(b": ")
                    if len(args) > 1:
                        if mode == "Image":
                            self.layers[-1][args[0]] = args[1:]
                        elif mode == "Scanner":
                            self.scanners[-1][args[0]] = args[1:]
                    if line == b"*File list end":
                        break
                # Take care of the all metadata
                try:
                    line = line.decode("ascii")
                except UnicodeDecodeError as e:
                    line = line.decode("latin1")

                if line.endswith(":"):
                    continue
                key_val = line.split(": ")

                if len(key_val) == 2 and not key_val[1]:
                    continue
                if key_val[0] == "*File list":
                    continue
                if len(key_val) == 1:
                    if got_leaf_key:
                        got_leaf_key = False
                        parent_key = ""
                    # Track how to admistrative name like: \*Ciao image list
                    last_admin_key_order = (
                        [key_val[0], 0]
                        if last_admin_key_order[0] != key_val[0]
                        else [last_admin_key_order[0], last_admin_key_order[1] + 1]
                    )

                    # If only one administrative key is found not extension otherwise exntend the key by order
                    parent_key = (
                        parent_key
                        + "/"
                        + (
                            key_val[0] + "_" + str(last_admin_key_order[1])
                            if last_admin_key_order[1] > 0
                            else key_val[0]
                        )
                    )
                else:
                    got_leaf_key = True
                    self.parsed_data[parent_key + "/" + key_val[0]] = key_val[1]

    def _get_bpp(self, i):
        return super(BrukerSPM, self)._get_bpp(i)

    def _get_raw_layer(self, i, debug=False, mock_data=False):
        return super(BrukerSPM, self)._get_raw_layer(i, debug, mock_data)

    def list_channels(self, encoding="latin1"):
        # super(BrukerSPM, self).list_channels(encoding)
        print("Channels")
        print("========")
        channel_list = []
        for layer in self.layers:
            with contextlib.suppress(KeyError):
                key = b"@2:Image Data"
                channel = (
                    key.decode(encoding=encoding)
                    + ": "
                    + layer[key][0].decode(encoding)
                )
                channel_list.append(channel)
                print(channel)
        for layer in self.layers:
            with contextlib.suppress(KeyError):
                key = b"@3:Image Data"
                channel = (
                    key.decode(encoding=encoding)
                    + ": "
                    + layer[key][0].decode(encoding)
                )
                channel_list.append(channel)
                print(layer[key][0].decode(encoding) + " (MFM)")
        return channel_list

    def _get_layer_val(self, index: int, name: str, first=True):
        return super(BrukerSPM, self)._get_layer_val(index, name, first)

    def _get_res(self, layer_index):
        return super(BrukerSPM, self)._get_res(layer_index)

    def _get_layer_size(self, layer_index, encoding, debug=False):
        return super(BrukerSPM, self)._get_layer_size(layer_index, encoding, debug)

    def get_channel_data(
        self,
        channel="Height Sensor",
        backward=False,
        corr=None,
        debug=False,
        encoding="latin1",
        mfm=False,
        mock_data=False,
    ):
        """
        Load the SPM image contained in a channel
        """
        for i in range(len(self.layers)):
            if mfm:
                # Handle case of MFM, where image data is stored at layer 3 on the backward channel
                backward = True
                _type = "Bruker MFM"
                try:
                    layer_name = self._get_layer_val(i, "@3:Image Data").decode(
                        encoding
                    )
                except KeyError:
                    continue
            else:
                _type = "Bruker AFM"
                try:
                    layer_name = self._get_layer_val(i, "@2:Image Data").decode(
                        encoding
                    )
                except KeyError:
                    continue
            result = re.match(r'([^ ]+) \[([^]]*)] "([^"]*)"', layer_name).groups()
            if result[2] == channel:
                if debug:
                    print("channel " + channel + " Found!")
                bck = False
                if self._get_layer_val(i, "Line Direction") == b"Retrace":
                    bck = True
                if bck == backward:
                    if debug:
                        print("Direction found")
                    var = self._get_layer_val(i, "@2:Z scale").decode(encoding)
                    if debug:
                        print("@2:Z scale", var)
                    if "[" in var:
                        result = re.match(
                            r"[A-Z]+\s+\[([^]]+)]\s+\(-?[0-9.]+ .*?\)\s+(-?[0-9.]+)\s+(.*?)$",
                            var,
                        ).groups()
                        if debug:
                            print(result)
                        bpp = int(self._get_layer_val(i, "Bytes/pixel"))
                        if debug:
                            print("BPP", bpp)
                        # scale = float(result[1])
                        scale = float(result[1]) / 256**bpp

                        result2 = self.scanners[0][b"@" + result[0].encode(encoding)][
                            0
                        ].split()
                        if debug:
                            print("result2", result2)
                        scale2 = float(result2[1])
                        zscale = result2[2] if len(result2) > 2 else result2[0]
                        if b"/V" in zscale:
                            zscale = zscale.replace(b"/V", b"")
                        if debug:
                            print(f"scale: {scale:.3e}")
                            print(f"scale2: {scale2:.3e}")
                            print("zscale: " + str(zscale))
                        var = self._get_layer_val(i, "@2:Z offset").decode(encoding)
                        result = re.match(
                            r"[A-Z]+\s+\[[^]]+]\s+\(-?[0-9.]+ .*?\)\s+(-?[0-9.]+)\s+.*?$",
                            var,
                        ).groups()
                        offset = float(result[0])
                    else:
                        if debug:
                            print("mode 2")
                        result = re.match(
                            r"[A-Z]+ \(-?[0-9.]+ [^)]+\)\s+(-?[0-9.]+) [\w]+", var
                        ).groups()
                        scale = float(result[0]) / 65536.0
                        scale2 = 1
                        zscale = b"V"
                        result = re.match(
                            r"[A-Z]+ \(-?[0-9.]+ .*?\)\s+(-?[0-9.]+) .*?",
                            self._get_layer_val(i, "@2:Z offset").decode(encoding),
                        ).groups()
                        offset = float(result[0])
                    if debug:
                        print("Offset:", offset)
                    data = (
                        self._get_raw_layer(i, debug=debug, mock_data=mock_data)
                        * scale
                        * scale2
                    )
                    xres, yres = self._get_res(i)
                    if debug:
                        print("xres/yres", xres, yres)
                    scan_size = self._get_layer_val(i, "Scan Size").split()
                    aspect_ratio = [
                        float(x)
                        for x in self._get_layer_val(i, "Aspect Ratio").split(b":")
                    ]
                    if debug:
                        print("aspect ratio", aspect_ratio)
                        print("scan size", scan_size)
                    if scan_size[2][0] == 126:
                        scan_size[2] = b"u" + scan_size[2][1:]
                    size = {
                        "x": float(scan_size[0]),
                        "y": float(scan_size[1]) * yres / xres,
                        "unit": scan_size[2].decode(encoding),
                    }
                    return {
                        "channel": [channel, "Topography"][channel == "Height Sensor"],
                        "BIN": data,
                        "real": size,
                        "_type": _type,
                        "zscale": zscale.decode(encoding),
                        "corr": corr,
                    }

    def get_channel_image(
        self,
        channel="Height Sensor",
        backward=False,
        corr=None,
        debug=False,
        encoding="latin1",
        lazy=True,
        mfm=False,
        mock_data=False,
    ):
        return super(BrukerSPM, self).get_channel(
            channel, backward, corr, debug, encoding, lazy, mfm, mock_data
        )
