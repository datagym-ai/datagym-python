from typing import Dict, List


class LabelConfig:

    def __init__(self):
        super().__init__()
        self.label_config = list()

    def toJson(self):
        export_list = [dict(item) for item in self.label_config]
        return export_list

    def append_entry(self, entry: "Label", overwrite_duplicate: bool = False) -> "Label":
        """
        Append entry to label config list. In case it already exists this step is skipped unless overwrite_duplicate
        is true
        :param entry: The desired new Label entry
        :param overwrite_duplicate: Decide if entry is skipped[false] or overwritten[true]
        in case of duplicate entry key.
        :return:
        """
        if entry not in self.label_config:
            self.label_config.append(entry)
            return entry
        else:
            identical_entry = [x for x in self.label_config if x == entry][0]

            if overwrite_duplicate:
                self.label_config.remove(identical_entry)
                self.label_config.append(entry)
                return entry
            else:
                return identical_entry

    def add_line(self,
                 entry_key: str,
                 entry_value: str,
                 children: List = None,
                 color: str = None,
                 shortcut: int = None
                 ) -> "Label":

        return self.append_entry(Line(entry_key, entry_value, children, color, shortcut))

    def add_point(self,
                  entry_key: str,
                  entry_value: str,
                  children: List = None,
                  color: str = None,
                  shortcut: int = None
                  ) -> "Label":

        return self.append_entry(Point(entry_key, entry_value, children, color, shortcut))

    def add_rectangle(self,
                      entry_key: str,
                      entry_value: str,
                      children: List = None,
                      color: str = None,
                      shortcut: int = None
                      ) -> "Label":
        return self.append_entry(Rectangle(entry_key, entry_value, children, color, shortcut))

    def add_polygon(self,
                    entry_key: str,
                    entry_value: str,
                    children: List = None,
                    color: str = None,
                    shortcut: int = None
                    ) -> "Label":
        return self.append_entry(Polygon(entry_key, entry_value, children, color, shortcut))

    def add_freetext(self,
                     entry_key: str,
                     entry_value: str,
                     max_length: int = 255,
                     children: List = None,
                     required: bool = False
                     ) -> "Label":
        return self.append_entry(FreeText(entry_key, entry_value, max_length, children, required))

    def add_select(self,
                   entry_key: str,
                   entry_value: str,
                   options_dict: Dict,
                   children: List = None,
                   required: bool = False
                   ) -> "Label":
        return self.append_entry(Select(entry_key, entry_value, options_dict, children, required))

    def add_checklist(self,
                      entry_key: str,
                      entry_value: str,
                      options_dict: Dict,
                      children: List = None,
                      required: bool = False
                      ) -> "Label":
        return self.append_entry(Checklist(entry_key, entry_value, options_dict, children, required))


class Label:
    def __init__(self, entry_key: str, entry_value: str, children: List = None):
        self.entry_key = entry_key
        self.entry_value = entry_value
        if children is None:
            self.children = list()
        else:
            self.children = children

    def __eq__(self, other):
        """
        Two instances of the same class are eaula if the entry key is identical
        :param other: The object that the class instance is compared with
        :return:
        """
        if not isinstance(other, Label):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.entry_key == other.entry_key

    def append_entry(self, entry: "Label", overwrite_duplicate: bool = False) -> "Label":
        """
        Append entry to label config list. In case it already exists this step is skipped unless overwrite_duplicate
        is true
        :param entry: The desired new Label entry
        :param overwrite_duplicate: Decide if entry is skipped[false] or overwritten[true]
        in case of duplicate entry key.
        :return:
        """
        if entry not in self.children:
            self.children.append(entry)
            return entry
        else:
            identical_entry = [x for x in self.children if x == entry][0]

            if overwrite_duplicate:
                self.children.remove(identical_entry)
                self.children.append(entry)
                return entry
            else:
                return identical_entry

    def add_freetext(self,
                     entry_key: str,
                     entry_value: str,
                     max_length: int = 255,
                     children: List = None,
                     required: bool = False
                     ):
        freetext = FreeText(entry_key, entry_value, max_length, children, required)
        self.children.append(freetext)
        return freetext

    def add_select(self,
                   entry_key: str,
                   entry_value: str,
                   options_dict: Dict,
                   children: List = None,
                   required: bool = False
                   ):
        select = Select(entry_key, entry_value, options_dict, children, required)
        self.children.append(select)
        return select

    def add_checklist(self,
                      entry_key: str,
                      entry_value: str,
                      options_dict: Dict,
                      children: List = None,
                      required: bool = False
                      ):
        checklist = Checklist(entry_key, entry_value, options_dict, children, required)
        self.children.append(checklist)
        return checklist

    def __iter__(self):
        yield "entryKey", self.entry_key
        yield "entryValue", self.entry_value
        yield "children", [dict(item) for item in self.children]


class Geometry(Label):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 children: List = None,
                 color: str = None,
                 shortcut: int = None
                 ):
        super().__init__(entry_key, entry_value, children)
        self.color = color
        if shortcut and 0 <= shortcut < 10:
            self.shortcut = shortcut
        else:
            self.shortcut = None

    def __iter__(self):
        yield from super().__iter__()
        if self.color:
            yield "color", self.color
        if self.shortcut:
            yield "shortcut", self.shortcut


class Rectangle(Geometry):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 children: List = None,
                 color: str = None,
                 shortcut: int = None
                 ):
        super().__init__(entry_key, entry_value, children, color, shortcut)

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "rectangle"


class Polygon(Geometry):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 children: List = None,
                 color: str = None,
                 shortcut: int = None
                 ):
        super().__init__(entry_key, entry_value, children, color, shortcut)

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "polygon"


class Line(Geometry):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 children: List = None,
                 color: str = None,
                 shortcut: int = None
                 ):
        super().__init__(entry_key, entry_value, children, color, shortcut)

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "line"


class Point(Geometry):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 children: List = None,
                 color: str = None,
                 shortcut: int = None
                 ):
        super().__init__(entry_key, entry_value, children, color, shortcut)

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "point"


class Classification(Label):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 children: List = None,
                 required: bool = False
                 ):
        super().__init__(entry_key, entry_value, children)
        self.required = required

    def __iter__(self):
        yield from super().__iter__()
        yield "required", self.required


class FreeText(Classification):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 max_length: int = 255,
                 children: List = None,
                 required: bool = False
                 ):
        super().__init__(entry_key, entry_value, children, required)
        self.max_length = max_length

    def __iter__(self):
        yield from super().__iter__()
        yield "maxLength", self.max_length
        yield "type", "freetext"


class Options(Classification):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 options_dict: Dict,
                 children: List = None,
                 required: bool = False
                 ):
        super().__init__(entry_key, entry_value, children, required)
        self.options = options_dict

    def __iter__(self):
        yield from super().__iter__()
        yield "options", self.options


class Checklist(Options):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 options_dict: Dict,
                 children: List = None,
                 required: bool = False
                 ):
        super().__init__(entry_key, entry_value, options_dict, children, required)

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "checklist"


class Select(Options):
    def __init__(self,
                 entry_key: str,
                 entry_value: str,
                 options_dict: Dict,
                 children: List = None,
                 required: bool = False
                 ):
        super().__init__(entry_key, entry_value, options_dict, children, required)

    def __iter__(self):
        yield from super().__iter__()
        yield "type", "select"
