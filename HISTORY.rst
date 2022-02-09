=======
History
=======

0.1.0 (2020-03-31)
------------------
* First release on PyPI.


0.2.0 (2020-04-06)
------------------
* Added Import Labels functionality.


0.3.0 (2020-04-27)
------------------
* Added coco importer
* Removed owner from dataset
* Url and Label upload in mini batches


0.4.0 (2020-04-27)
------------------
* Added warnings for non fatal exceptions
* Added image upload functionality


0.5.0 (2020-06-09)
------------------
* Added a label config uploader
* Adjusted the coco uploader to work together with the label config uploader


0.5.1 (2020-08-26)
------------------
* Added dependencies to allow requests to deal with 104 error codes


0.5.2 (2021-03-15)
------------------
* Changed *_image_id to *_media_id in label imports/exports


0.6.0 (2021-05-19)
------------------
* Added Video functionalities
* Renamed most instances of image_id to media_id to allow agnostic media usage

0.7.0 (2022-02-07)
------------------
* Adjust endpoints: Token in URL, BasicAuth as request parameter

0.7.1 (2022-02-07)
------------------
* Upgrade numpy to 1.22.2, upgrade opencv-python to 4.5.5.62

0.7.2 (2022-02-09)
------------------
* Tab indent fix