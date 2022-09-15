import time

from mediahaven import MediaHaven
from mediahaven.oauth2 import ROPCGrant, RequestTokenError
from prefect import task, get_run_logger

@task()
def query_mediahaven( client: MediaHaven, q, last_modified_date=None, start_index=0, nr_of_results=100):
    records_page = client.records.search(q=q, nrOfResults=nr_of_results, startIndex=start_index, LastModifiedDate=last_modified_date)
    return records_page


@task()
def update_mediahaven(client: MediaHaven, fragment_id, json=None, xml=None):
    time.sleep(1)
    logger = get_run_logger()
    resp = None
    try:
        resp = client.records.update(record_id=fragment_id, json=json, xml=xml)
        logger.info(f"Updated {fragment_id}")
    except Exception as e:
        logger.warning(e)
        logger.warning("Not updated: " + fragment_id)
    return resp

# @task()
# def generate_mediahaven_json(to_update : dict):
#     {
# 	"Administrative": {
# 		"LastModifiedDate": "2022-09-14T14:45:50.153000Z",
# 		"IsSynchronized": false,
# 		"OrganisationName": "kuleuvenkadoc",
# 		"Workflow": "SONIM",
# 		"ArchiveDate": "2015-02-10T20:47:35.000000Z",
# 		"IngestTape": "IM0181L5",
# 		"RecordStatus": "Published",
# 		"IsAccess": false,
# 		"Type": "audio",
# 		"IsOriginal": true,
# 		"IsPreservation": false,
# 		"DepartmentName": "kuleuvenkadoc",
# 		"UserLastModifiedDate": "2022-09-14T14:45:50.153000Z",
# 		"OrganisationLongName": "kuleuvenkadoc",
# 		"RecordType": "Record",
# 		"PublicationDate": "2022-05-16T21:41:02.618000Z",
# 		"ExternalId": "b853f4mw96",
# 		"DeleteStatus": "NotDeleted",
# 		"MainRecordType": "Record",
# 		"OrganisationExternalId": "OR-3x83k1b",
# 		"ExternalUrl": null,
# 		"LogicalDeletionDate": null,
# 		"ChildOrderFields": {},
# 		"RejectionDate": null,
# 		"ExternalUse": null
# 	},
# 	"Dynamic": {
# 		"OTC_start": "00:00:00.000",
# 		"old_title": "BE/942855/394/2771-2772",
# 		"type_viaa": "Audio",
# 		"audio_iec_type": "II",
# 		"brand": "TDK",
# 		"audio_tracks": "2",
# 		"iec_type": "II",
# 		"inspection_outcome": "y",
# 		"batch_pickup_date": "2014-09-16",
# 		"shipment_id": "14103468961",
# 		"digitization_format": "WAV",
# 		"filename": "b853f4mw96.wav",
# 		"created_on": "2014-09-09T09:09:09",
# 		"updated_by": "Loes Nijsmans",
# 		"status": "Checked in at SP",
# 		"qc_date": "2014-12-22",
# 		"batch_id": "ACCB09",
# 		"player_model": "2C",
# 		"inspection_date": "2014-09-22",
# 		"qc_outcome": "y",
# 		"is_preserved_by_another": "0",
# 		"dc_identifier_localid": "BE/942855/394/2771-2772",
# 		"PID": "b853f4mw96",
# 		"CP": "KADOC",
# 		"batch_name": "ACCB09",
# 		"dc_rights_licenses": {
# 			"multiselect": [
# 				"VIAA-ONDERWIJS",
# 				"VIAA-ONDERZOEK",
# 				"VIAA-INTRA_CP-CONTENT",
# 				"VIAA-INTRA_CP-METADATA-ALL",
# 				"VIAA-PUBLIEK-METADATA-LTD",
# 				"BEZOEKERTOOL-CONTENT",
# 				"BEZOEKERTOOL-METADATA-ALL"
# 			]
# 		},
# 		"player_serial_number": "5",
# 		"carrier_barcode": "AACC_KAD_000632",
# 		"preservation_problems": "Geen",
# 		"updated_on": "2014-09-09T09:09:09",
# 		"date": "1997-uu-uu",
# 		"noise_reduction": "Onbekend",
# 		"md5_viaa": "f389e9e977f4b24fb182bf0dbdfcd7d0",
# 		"lto_id": "IM0181L5",
# 		"player_manufacturer": "Plusdeck",
# 		"digitization_date": "2014-11-04",
# 		"transfer_lto_date": "2014-12-18",
# 		"digitization_outcome": "y",
# 		"digitization_time": "15:36:27",
# 		"format": "Audiocassette",
# 		"AD_model": "Alc887",
# 		"created_by": "Loes Nijsmans",
# 		"AD_manufacturer": "Realtek",
# 		"sp_id": "OR-c824d3c",
# 		"dcterms_created": "1997",
# 		"qc_by": "User001",
# 		"duration": "01:00:00",
# 		"sp_name": "SONIM",
# 		"file_duration": "01:06:00.000",
# 		"transport_box_barcode": "SONIM165",
# 		"audio_carrier_speed": "4.75 cm/s",
# 		"AD_serial_number": "5",
# 		"original_carrier_id": "BE/942855/394/2771-2772",
# 		"CP_id": "OR-3x83k1b",
# 		"collection_box_barcode": "BACC_KAD_000008",
# 		"NeedsPublicationDateMigration": "true"
# 	},
# 	"Internal": {
# 		"PathToVideo": "https://archief-media.viaa.be/viaa/KULEUVENKADOC/e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c/browse.mp4",
# 		"PathToKeyframe": "https://archief-media.viaa.be/viaa/KULEUVENKADOC/e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c/keyframes/keyframes_1_1/keyframe1.jpg",
# 		"PathToPreview": "https://archief-media.viaa.be/viaa/KULEUVENKADOC/e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c/browse.mp4",
# 		"Browses": {
# 			"Browse": [
# 				{
# 					"BaseUrl": "https://archief-media.viaa.be/viaa/KULEUVENKADOC/e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c",
# 					"PathToKeyframe": "keyframes/keyframes_1_1/keyframe1.jpg",
# 					"PathToKeyframeThumb": "keyframes-thumb/keyframes_1_1/keyframe1.jpg",
# 					"PathToVideo": "browse.mp4",
# 					"HasKeyframes": true,
# 					"Container": "mp3",
# 					"Label": "mp3",
# 					"FileSize": 0
# 				},
# 				{
# 					"BaseUrl": "https://archief-media.viaa.be/viaa/KULEUVENKADOC/e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c",
# 					"PathToKeyframe": "keyframes/keyframes_1_1/keyframe1.jpg",
# 					"PathToKeyframeThumb": "keyframes-thumb/keyframes_1_1/keyframe1.jpg",
# 					"PathToVideo": "browse.m4a",
# 					"HasKeyframes": true,
# 					"Container": "m4a",
# 					"Label": "m4a",
# 					"FileSize": 0
# 				}
# 			]
# 		},
# 		"BrowseStatus": "completed",
# 		"RecordId": "e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c",
# 		"IsInIngestSpace": false,
# 		"OrganisationId": "115",
# 		"ContainsGeoData": false,
# 		"OriginalStatus": "completed",
# 		"IsFragment": false,
# 		"HasKeyframes": true,
# 		"MediaObjectId": "e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c",
# 		"ArchiveStatus": "on_tape",
# 		"FragmentId": "e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8cefd1561500eb2024a4c2052b8a0fcb3e",
# 		"PathToKeyframeThumb": "https://archief-media.viaa.be/viaa/KULEUVENKADOC/e4860d02f8564602a1293bb98db1193ea9256b73231a4fb4a0a2ed89d3c5ef8c/keyframes-thumb/keyframes_1_1/keyframe1.jpg",
# 		"DepartmentId": "dd115b7a-efd0-44e3-8816-0905572421da",
# 		"IngestSpaceId": null,
# 		"UploadedById": null,
# 		"Distributions": {
# 			"Distribution": []
# 		},
# 		"Profiles": {}
# 	},
# 	"Structural": {
# 		"HasChildren": false,
# 		"FragmentStartFrames": 0,
# 		"FragmentStartTimeCode": "00:00:00.000",
# 		"FragmentEndTimeCode": "01:06:00.000",
# 		"FragmentDurationFrames": 99000,
# 		"FragmentDurationTimeCode": "01:06:00.000",
# 		"FragmentEndFrames": 99000,
# 		"Versioning": {
# 			"Status": "Untracked",
# 			"Version": 1
# 		},
# 		"Collections": {
# 			"Collection": []
# 		},
# 		"Sets": {
# 			"Set": []
# 		},
# 		"Newspapers": {
# 			"Newspaper": []
# 		},
# 		"Relations": {},
# 		"Fragments": {
# 			"Fragment": []
# 		},
# 		"MainFragment": null,
# 		"ReferenceCodes": {},
# 		"ParentRecordId": null,
# 		"ReferenceTitles": {},
# 		"FieldDefinition": {},
# 		"PreviewRecordId": null
# 	},
# 	"RightsManagement": {
# 		"Permissions": {
# 			"Write": [
# 				"cc7c56fc-58c8-4650-bc63-7e695fbc506c",
# 				"dc100b7a-efd0-44e3-8816-0905572421da",
# 				"dd115b7a-efd0-44e3-8816-0905572421da",
# 				"eb812a36-48d9-41e1-87f9-a859a5af8c96"
# 			],
# 			"Export": [
# 				"cc7c56fc-58c8-4650-bc63-7e695fbc506c",
# 				"dc100b7a-efd0-44e3-8816-0905572421da",
# 				"dd115b7a-efd0-44e3-8816-0905572421da",
# 				"eb812a36-48d9-41e1-87f9-a859a5af8c96"
# 			],
# 			"Read": [
# 				"cc7c56fc-58c8-4650-bc63-7e695fbc506c",
# 				"dc100b7a-efd0-44e3-8816-0905572421da",
# 				"dd115b7a-efd0-44e3-8816-0905572421da",
# 				"df115b7a-efd0-44e3-8816-0905572421da",
# 				"eb812a36-48d9-41e1-87f9-a859a5af8c96"
# 			]
# 		},
# 		"ExpiryDate": null,
# 		"ExpiryStatus": null,
# 		"Zone": {}
# 	},
# 	"Technical": {
# 		"OriginalExtension": "wav",
# 		"DurationFrames": 99000,
# 		"EndFrames": 99000,
# 		"MimeType": "audio/x-wav",
# 		"StartFrames": 0,
# 		"Md5": "f389e9e977f4b24fb182bf0dbdfcd7d0",
# 		"BitRate": 1536000,
# 		"AudioCodec": "pcm_s16le ([1][0][0][0] / 0x0001)",
# 		"AudioSampleRate": 48000,
# 		"FileSize": 760320044,
# 		"DurationTimeCode": "01:06:00.000",
# 		"EndTimeCode": "01:06:00.000",
# 		"AudioBitRate": 1536000,
# 		"StartTimeCode": "00:00:00.000",
# 		"PronomId": null,
# 		"Width": null,
# 		"Height": null,
# 		"ImageSize": null,
# 		"ImageOrientation": null,
# 		"ImageQuality": null,
# 		"VideoTechnical": null,
# 		"AudioTechnical": null,
# 		"VideoFormat": null,
# 		"Exif": {},
# 		"VideoCodec": null,
# 		"VideoFps": null,
# 		"VideoBitRate": null,
# 		"AudioChannels": null,
# 		"AudioTracks": {},
# 		"Origin": null,
# 		"EssenceOffset": null,
# 		"EditUnitByteSize": null,
# 		"RunIn": null,
# 		"FramesPerEditUnit": null,
# 		"EditRate": null,
# 		"IndexEditRate": null
# 	},
# 	"Descriptive": {
# 		"CreationDate": "1996-12-31T23:00:00.000000Z",
# 		"OriginalFilename": "b853f4mw96.wav",
# 		"RightsOwner": "© kadoc",
# 		"UploadedBy": "BulkUpload kadoc",
# 		"KeyframeStart": 0,
# 		"Title": "BE/942855/394/2771-2772",
# 		"Description": null,
# 		"CreationDateLegacy": null,
# 		"Rights": null,
# 		"Keywords": {
# 			"Keyword": []
# 		},
# 		"Categories": {
# 			"Category": []
# 		},
# 		"LimitedCategories": {},
# 		"Publisher": null,
# 		"Authors": {},
# 		"Location": null,
# 		"Address": {},
# 		"NonPreferredTerm": null,
# 		"Publications": {
# 			"Comment": []
# 		},
# 		"OriginalPath": null,
# 		"Position": {}
# 	},
# 	"Context": {
# 		"IsEditable": true,
# 		"IsDeletable": true,
# 		"IsPublic": false,
# 		"IsExportable": true,
# 		"Profiles": []
# 	}
# }