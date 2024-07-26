from pySPM.Bruker import Bruker
from typing import Any


class BrukerSPM(Bruker):
    def __init__(self, path):
        self.path = path
        # After with the parent pat the leaf key will be added.
        parent_key = ""
        # Last part of the administrative path
        last_admin_key_order = ["", 0]
        got_leaf_key = False

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
                line = line.decode("utf-8")
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
        super(BrukerSPM, self).list_channels(encoding)

    def _get_layer_val(self, index: int, name: str, first=True):
        return super(BrukerSPM, self)._get_layer_val(index, name, first)

    def _get_res(self, layer_index):
        return super(BrukerSPM, self)._get_res(layer_index)

    def _get_layer_size(self, layer_index, encoding, debug=False):
        return super(BrukerSPM, self)._get_layer_size(layer_index, encoding, debug)

    def get_channel(
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
