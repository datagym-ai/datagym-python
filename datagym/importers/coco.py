from typing import Dict, Tuple, List
import cv2
from ..utils.coco_utils import add_to_dict_valuelist, decodeMask


class CocoImage:
    """
    The CocoImage class is the collection of all the information that
    is provided in multiple coco format json files.
    """

    def __init__(self, file_name: str, coco_image_id: str, width: int, height: int, coco_url: str = None) -> None:
        """
        The CocoImage class collects these attributes for each image instance.
        :param str file_name: The filename of the image within the filesystem
        :param str coco_image_id: The coco_image_id that is used to ssign instances and captions to an image
        :param int width: The image width
        :param int height: The image height
        :param str coco_url: The download url if available
        """
        self.file_name = file_name
        self.coco_image_id = coco_image_id
        self.width = width
        self.height = height
        if coco_url:
            self.coco_url = coco_url
        self.annotations = {}
        self.classifications = {}

    def __repr__(self):
        return f'<Image {self.__dict__}>'

    def get_shape(self) -> Tuple:
        """
        Gets the shape of the image as a tuple (w, h)
        :return: (w, h)
        """
        shape = (self.width, self.height)
        return shape

    def add_annotation(self, label_entry: List, annotation_supercategory: str) -> None:
        """
        Add one annotation from the annotation list in the json to the annotations dictionary.
        :param label_entry:
        :param annotation_supercategory:
        :return: None
        """
        self.annotations = add_to_dict_valuelist(
            dictionary=self.annotations,
            key=annotation_supercategory,
            value=label_entry
        )

    def datagymify(self, image_ids_dict: Dict) -> Dict:
        """
        Convert all labels on an image into a datagym compatible entry for the upload json
        :param Dict image_ids_dict: Image ids dict with { image_name : coco_img_id, ...}
        :return: image entry as dict if image in image_ids_dict
        """
        if self.file_name in image_ids_dict:
            internal_media_ID = image_ids_dict[self.file_name]
            image_entry = {
                "internal_media_ID": internal_media_ID,
                "keepData": False,
                # "image_name": self.file_name,
                "global_classifications": self.classifications,
                "labels": self.annotations
            }
            return image_entry
        else:
            return None


class Coco:
    """
    The coco class is used to convert coco format labels into datagym format
    """

    def __init__(self) -> None:
        self.instances_supercategories = {}
        self.category_dict = {}
        self.coco_images = {}

    def get_datagym_label_dict(self, image_ids_dict: Dict) -> Dict:
        """
        Use this method once you have added your json data to return a json upload object in datagym format
        :param image_ids_dict:  Image ids dict with { image_name : coco_img_id, ...}
        :return: Datagym json upload object
        """

        upload_json = []

        for image in self.coco_images.values():
            image_entry = image.datagymify(image_ids_dict)
            if image_entry:
                upload_json.append(image_entry)

        return upload_json

    def add_object_detection_data(self, json_data: Dict, polygon: bool = False) -> None:
        """
        Use this method to add the instances json contents to your coco instance for later conversion
        :param Dict json_data: Json data loaded from your instances json file
        :param polygon: Boolean to decide whether to use the bbox (false) or the polygon (true)
        :return: None
        """
        self.__get_coco_object_categories(json_data)
        self.__get_coco_images(json_data)

        if polygon:
            self.__process_coco_polygons(json_data)
        else:
            self.__process_coco_bbox(json_data)

    def add_captions_data(self, json_data: Dict) -> None:
        """
        Use this method to add the captions json contents to your coco instance for later conversion
        :param Dict json_data: Json data loaded from your instances json file
        :return: None
        """
        self.__get_coco_images(json_data)
        self.__process_coco_caption(json_data)

    def __process_coco_polygons(self, instances_data: Dict) -> None:
        """
        Based on the instances json add the coco polygon instances to the respective CocoImage instance
        :param instances_data: Json data loaded from your instances json file
        :return: None
        """
        for annotation in instances_data["annotations"]:
            annotation_supercategory = self.category_dict[annotation["category_id"]]["supercategory"]
            annotation_name = self.category_dict[annotation["category_id"]]["name"]

            if annotation["iscrowd"] == 0:
                polygon = []
                it = iter(annotation["segmentation"][0])
                for x, y in zip(it, it):
                    polygon.append({"x": x, "y": y})

                label_entry = {
                    "geometry": polygon,
                    "classifications": {"subcategory": [annotation_name]}
                }

                self.coco_images[annotation["image_id"]].add_annotation(label_entry, annotation_supercategory)

            elif "size" in annotation["segmentation"]:
                annotation_RLE = annotation["segmentation"]
                mask = decodeMask(annotation_RLE)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contours:
                    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

                    polygon = [{"x": int(point[0][0]), "y": int(point[0][1])} for point in approx]

                    label_entry = {
                        "geometry": polygon,
                        "classifications": {"subcategory": [annotation_name]}
                    }

                    self.coco_images[annotation["image_id"]].add_annotation(label_entry, annotation_supercategory)

    def __process_coco_bbox(self, instances_data: Dict) -> None:
        """
        Based on the instances json add the coco bbox instances to the respective CocoImage instance
        :param instances_data: Json data loaded from your instances json file
        :return: None
        """
        for annotation in instances_data["annotations"]:
            annotation_supercategory = self.category_dict[annotation["category_id"]]["supercategory"]
            annotation_name = self.category_dict[annotation["category_id"]]["name"]
            rectangle = {
                "x": annotation["bbox"][0],
                "y": annotation["bbox"][1],
                "w": annotation["bbox"][2],
                "h": annotation["bbox"][3]
            }
            label_entry = {
                "geometry": [rectangle],
                "classifications": {"subcategory": [annotation_name]}
            }

            self.coco_images[annotation["image_id"]].add_annotation(label_entry, annotation_supercategory)

    def __process_coco_caption(self, captions_data: Dict) -> None:
        """
        Based on the captions json add the image caption to the respective CocoImage instance
        :param captions_data: Json data loaded from your instances json file
        :return: None
        """
        for annotation in captions_data["annotations"]:

            self.coco_images[annotation["image_id"]].classifications["caption"] = [annotation["caption"]]

    def __get_coco_images(self, images_data: Dict) -> None:
        """
        Fill the coco_images dict based on all the images inside your coco json file
        :param images_data: Json data loaded from your coco json file
        :return: None
        """
        for image in images_data["images"]:
            if "coco_url" in image.keys():
                value = CocoImage(
                        file_name=image["file_name"],
                        coco_image_id=image["id"],
                        width=image["width"],
                        height=image["height"],
                        coco_url=image["coco_url"]
                )
            else:
                value = CocoImage(
                    file_name=image["file_name"],
                    coco_image_id=image["id"],
                    width=image["width"],
                    height=image["height"]
                )

            if image["id"] not in self.coco_images:
                self.coco_images[image["id"]] = value

    def __get_coco_object_categories(self, instances_data: Dict) -> None:
        """
        Fill the coco category dict based on all the categories inside your coco json file
        :param instances_data: Json data loaded from your coco json file
        :return: None
        """
        for category in instances_data["categories"]:

            key = category["supercategory"]
            value = category["name"]

            self.instances_supercategories = add_to_dict_valuelist(
                dictionary=self.instances_supercategories,
                key=key,
                value=value
            )

            self.category_dict[category["id"]] = dict(name=category["name"], supercategory=category["supercategory"])
