""" Date Format """
DT_FMT_dmy = '%d/%m/%y'  # 31/12/17
DT_FMT_bdYIMp = '%b %d %Y %I:%M %p'  # Jul 16 2017 08:46 PM
DT_FMT_ymdHMSf = '%Y-%m-%d %H:%M:%S.%f'  # 2017-07-19 06:58:20.370
DT_FMT_ymdHMSfz = '%Y-%m-%d %H:%M:%S.%f%z'  # 2017-07-19 06:58:20.370+00:00
DT_FMT_ymdHMS = '%Y-%m-%d %H:%M:%S'  # 2017-07-19 06:58:20
DT_FMT_Ymd = '%Y-%m-%d'  # 2017-09-11
DT_FMT_YMD = '%Y/%m/%d'
DT_FMT_ymdHM = '%Y-%m-%d %H:%M'
DT_FMT_dbYHMS = '%d-%b-%Y %H:%M:%S'
DT_FMT_dbYHMSf = '%d-%b-%Y %H:%M:%S.%f'
DT_FMT_HM = '%H:%M'
DT_FMT_HMSf = '%H%M%S%f'
DT_FMT_dmY = '%d/%m/%Y'
DT_FMT_HMS = '%H:%M:%S' # 02:23:45
DT_FMT_ymdTHMS = '%Y-%m-%dT%H:%M:%S'  # 2017-07-19T06:58:20
DT_FMT_ymdTHMSf = '%Y-%m-%dT%H:%M:%S.%f'  # 2017-07-19T06:58:20.123543
DT_FMT_ymdTH = '%Y-%m-%dT%H:00:00'  # 2023-04-04T06:00:00

GCP_STORAGE_HOST_URL = 'https://{bucket_name}.storage.googleapis.com'
S3_STORAGE_HOST_URL = "https://{bucket_name}.s3.{region_name}.amazonaws.com"
LOCAL_STORAGE_URL = "{host}/v1/media"
AZURE_STORAGE_URL = "https://{account_name}.blob.core.windows.net"

SMALL_IMAGE_KEY = '_thumb_'

""" Variables """
VARIABLE_PREFIX_MATCHING_SEQUENCE = ['¿·$user.info.', '¿·$user.', '¿·']
VARIABLE_PREFIX_AND_TYPE_MAPPING = {
    '¿·$user.info.': 'contact',
    '¿·$user.': 'system',
    '¿·': 'custom'
}

VARIABLE_PREFIX_AND_TYPE_MAPPINGS = {
    '¿·$user.info.': 'contact',
    '¿·$user.': 'system',
    '¿·': 'conversation'
}
VARIABLE_PATTERNS_TO_BE_REPLACED = VARIABLE_PREFIX_MATCHING_SEQUENCE + ['·?']

"""Language codes"""
ARABIC_LANGUAGE_CODE = 'ar'

"""English to another language numeric mapping"""

NUMERIC_ENGLISH_TO_ARABIC_MAPPING = {
    "0": "٠",
    "1": "١",
    "2": "٢",
    "3": "٣",
    "4": "٤",
    "5": "٥",
    "6": "٦",
    "7": "٧",
    "8": "٨",
    "9": "٩"
}

NUMERIC_ENGLISH_TO_URDU_MAPPING = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹"
}

"""Urdu numeric to word mapping"""
URDU_NUMERIC_TO_WORD_MAPPING = {
    "1": "ایک",
    "2": "دو",
    "3": "تین",
    "4": "چار",
    "5": "پانچ",
    "6": "چھ",
    "7": "سات",
    "8": "آٹھ",
    "9": "نو",
    "10": "دس",
    "11": "گیارہ",
    "12": "بارہ",
    "13": "تیرہ",
    "14": "چودہ",
    "15": "پندرہ",
    "16": "سولہ",
    "17": "سترہ",
    "18": "اٹھارہ",
    "19": "انیس",
    "20": "بیس"
}

#  Invalid Request Error message
INVALID_REQUEST_ERROR_MESSAGE = "Error raised while invoking {}"

FREE_TRIAL_YEAR = 2100

CONTACT_VARIABLE_PREFIX = '$user.info.'
NON_CONTACT_VARIABLE_PRE_POST_FIX = '#'
NON_CONTACT_VARIABLE_PREFIX_V2 = '¿·'
NON_CONTACT_VARIABLE_POSTFIX_V2 = '·?'
VARIABLE_PATTERN_REGEX = r'(\$user\.info\.|·\?|¿·|#)'
ALLOWED_VARIABLE_CHARACTERS = r'^[a-z0-9_]+$'
MIMETYPES = {'js': 'application/javascript', 'mjs': 'application/javascript', 'json': 'application/json',
             'webmanifest': 'application/manifest+json', 'doc': 'application/msword', 'dot': 'application/msword',
             'wiz': 'application/msword', 'bin': 'application/octet-stream', 'a': 'application/octet-stream',
             'dll': 'application/x-msdownload', 'exe': 'application/x-msdownload', 'o': 'application/octet-stream',
             'obj': 'application/octet-stream', 'so': 'application/octet-stream', 'oda': 'application/oda',
             'pdf': 'application/pdf', 'p7c': 'application/pkcs7-mime', 'ps': 'application/postscript',
             'ai': 'application/postscript', 'eps': 'application/postscript', 'm3u': 'audio/x-mpegurl',
             'm3u8': 'application/vndapplempegurl', 'xls': 'application/vndms-excel',
             'xlb': 'application/vndms-excel', 'ppt': 'application/vndms-powerpoint',
             'pot': 'application/vndms-powerpoint', 'ppa': 'application/vndms-powerpoint',
             'pps': 'application/vndms-powerpoint', 'pwz': 'application/vndms-powerpoint',
             'wasm': 'application/wasm', 'bcpio': 'application/x-bcpio', 'cpio': 'application/x-cpio',
             'csh': 'text/plain', 'dvi': 'application/x-dvi', 'gtar': 'application/x-gtar',
             'hdf': 'application/x-hdf', 'latex': 'application/x-latex', 'mif': 'application/x-mif',
             'cdf': 'application/x-netcdf', 'nc': 'application/x-netcdf', 'p12': 'application/x-pkcs12',
             'pfx': 'application/x-pkcs12', 'ram': 'application/x-pn-realaudio', 'pyc': 'application/x-python-code',
             'pyo': 'application/x-python-code', 'sh': 'application/x-sh', 'shar': 'application/x-shar',
             'swf': 'application/x-shockwave-flash', 'sv4cpio': 'application/x-sv4cpio',
             'sv4crc': 'application/x-sv4crc', 'tar': 'application/x-tar', 'tcl': 'application/x-tcl',
             'tex': 'application/x-tex', 'texi': 'application/x-texinfo', 'texinfo': 'application/x-texinfo',
             'roff': 'application/x-troff', 't': 'application/x-troff', 'tr': 'application/x-troff',
             'man': 'application/x-troff-man', 'me': 'application/x-troff-me', 'ms': 'application/x-troff-ms',
             'ustar': 'application/x-ustar', 'src': 'application/x-wais-source', 'xsl': 'text/xml',
             'rdf': 'application/xml', 'wsdl': 'application/xml', 'xpdl': 'application/xml',
             'zip': 'application/x-zip-compressed', 'au': 'audio/basic', 'snd': 'audio/basic', 'mp3': 'audio/mpeg',
             'mp2': 'audio/mpeg', 'aif': 'audio/aiff', 'aifc': 'audio/aiff', 'aiff': 'audio/aiff',
             'ra': 'audio/x-pn-realaudio', 'wav': 'audio/wav', 'bmp': 'image/bmp', 'gif': 'image/gif',
             'ief': 'image/ief', 'jpg': 'image/jpeg', 'jpe': 'image/jpeg', 'jpeg': 'image/jpeg',
             'png': 'image/png', 'svg': 'image/svg+xml', 'tiff': 'image/tiff', 'tif': 'image/tiff',
             'ico': 'image/x-icon', 'ras': 'image/x-cmu-raster', 'pnm': 'image/x-portable-anymap',
             'pbm': 'image/x-portable-bitmap', 'pgm': 'image/x-portable-graymap', 'ppm': 'image/x-portable-pixmap',
             'rgb': 'image/x-rgb', 'xbm': 'image/x-xbitmap', 'xpm': 'image/x-xpixmap', 'xwd': 'image/x-xwindowdump',
             'eml': 'message/rfc822', 'mht': 'message/rfc822', 'mhtml': 'message/rfc822', 'nws': 'message/rfc822',
             'css': 'text/css', 'csv': 'application/vndms-excel', 'html': 'text/html', 'htm': 'text/html',
             'txt': 'text/plain', 'bat': 'text/plain', 'c': 'text/plain', 'h': 'text/plain', 'ksh': 'text/plain',
             'pl': 'text/plain', 'rtx': 'text/richtext', 'tsv': 'text/tab-separated-values', 'py': 'text/x-python',
             'etx': 'text/x-setext', 'sgm': 'text/x-sgml', 'sgml': 'text/x-sgml', 'vcf': 'text/x-vcard',
             'xml': 'text/xml', 'mp4': 'video/mp4', 'mpeg': 'video/mpeg', 'm1v': 'video/mpeg', 'mpa': 'audio/mpeg',
             'mpe': 'video/mpeg', 'mpg': 'video/mpeg', 'mov': 'video/quicktime', 'qt': 'video/quicktime',
             'webm': 'video/webm', 'avi': 'video/avi', 'movie': 'video/x-sgi-movie', '3fr': 'image/3FR',
             '3g2': 'video/3gpp2', '3gp': 'video/3gpp', '3gp2': 'video/3gpp2', '3gpp': 'video/3gpp',
             'aac': 'audio/vnddlnaadts', 'ac3': 'audio/vnddolbydd-raw',
             'accountpicture-ms': 'application/windows-accountpicture',
             'acrobatsecuritysettings': 'application/vndadobeacrobat-security-settings',
             'adt': 'audio/vnddlnaadts', 'adts': 'audio/vnddlnaadts', 'alc': 'chemical/x-alchemy',
             'androidproj': 'Application/xml', 'appcontent-ms': 'application/windows-appcontent+xml',
             'application': 'application/x-ms-application', 'ari': 'image/ARI', 'arw': 'image/ARW',
             'asd': 'application/msword', 'asf': 'video/x-ms-asf', 'asm': 'text/plain', 'asx': 'video/x-ms-asf',
             'bay': 'image/BAY', 'C3D': 'chemical/chem3d', 'cap': 'image/CAP',
             'cat': 'application/vndms-pkiseccat', 'cc': 'text/plain', 'cc1': 'chemical/x-cart1',
             'cc2': 'chemical/x-cart2', 'cdx': 'chemical/x-cdx', 'cdxml': 'chemical/x-cdxml',
             'cer': 'application/x-x509-ca-cert', 'cod': 'text/plain', 'config': 'application/xml',
             'contact': 'text/x-ms-contact', 'coverage': 'application/xml', 'cpp': 'text/plain',
             'cppm': 'text/plain', 'cr2': 'image/CR2', 'cr3': 'image/CR3', 'crl': 'application/pkix-crl',
             'crt': 'application/x-x509-ca-cert', 'crw': 'image/CRW', 'cs': 'text/plain', 'cshader': 'text/plain',
             'csproj': 'application/xml', 'cub': 'chemical/x-gaussian-cube', 'cxx': 'text/plain',
             'dat': 'chemical/x-ccdb', 'datasource': 'application/xml', 'dcr': 'image/DCR', 'dcs': 'image/DCS',
             'dds': 'image/vndms-dds', 'def': 'text/plain', 'der': 'application/x-x509-ca-cert',
             'dib': 'image/bmp', 'dng': 'image/DNG', 'docm': 'application/vndms-worddocumentmacroEnabled12',
             'docx': 'application/vndopenxmlformats-officedocumentwordprocessingmldocument',
             'dotm': 'application/vndms-wordtemplatemacroEnabled12',
             'dotx': 'application/vndopenxmlformats-officedocumentwordprocessingmltemplate', 'drf': 'image/DRF',
             'dsh': 'text/plain', 'dshader': 'text/plain', 'dsp': 'text/plain', 'dsw': 'text/plain',
             'dtcp-ip': 'application/x-dtcp1', 'dtd': 'application/xml-dtd', 'dvr-ms': 'video/x-ms-dvr',
             'dwfx': 'model/vnddwfx+xps', 'easmx': 'model/vndeasmx+xps', 'ec3': 'audio/ec3',
             'edrwx': 'model/vndedrwx+xps', 'eip': 'image/EIP', 'emf': 'image/x-emf',
             'eprtx': 'model/vndeprtx+xps', 'epub': 'application/epub+zip', 'erf': 'image/ERF',
             'fch': 'chemical/x-gaussian-checkpoint', 'fdf': 'application/vndfdf', 'fff': 'image/FFF',
             'fif': 'application/fractals', 'filters': 'text/plain', 'flac': 'audio/x-flac', 'fx': 'text/plain',
             'generictest': 'application/xml', 'gjc': 'chemical/x-gaussian-input-c3d',
             'gjf': 'chemical/x-gaussian-input', 'gpt': 'chemical/x-mopac-graph', 'group': 'text/x-ms-group',
             'gsh': 'text/plain', 'gshader': 'text/plain', 'gz': 'application/x-gzip', 'hh': 'text/plain',
             'hlsl': 'text/plain', 'hlsli': 'text/plain', 'hpp': 'text/plain', 'hqx': 'application/mac-binhex40',
             'hsh': 'text/plain', 'hshader': 'text/plain', 'hta': 'application/hta', 'htc': 'text/x-component',
             'hxa': 'application/xml', 'hxc': 'application/xml', 'hxd': 'application/octet-stream',
             'hxe': 'application/xml', 'hxf': 'application/xml', 'hxh': 'application/octet-stream',
             'hxi': 'application/octet-stream', 'hxk': 'application/xml', 'hxq': 'application/octet-stream',
             'hxr': 'application/octet-stream', 'hxs': 'application/octet-stream', 'hxt': 'application/xml',
             'hxv': 'application/xml', 'hxw': 'application/octet-stream', 'hxx': 'text/plain', 'i': 'text/plain',
             'idl': 'text/plain', 'iiq': 'image/IIQ', 'inc': 'text/plain', 'inl': 'text/plain',
             'inp': 'chemical/gamess-input', 'int': 'chemical/internal', 'ipp': 'text/plain',
             'iqy': 'text/x-ms-iqy', 'ixx': 'text/plain', 'jfif': 'image/jpeg',
             'jnlp': 'application/x-java-jnlp-file', 'jsproj': 'text/plain', 'jtx': 'application/x-jtx+xps',
             'jxr': 'image/vndms-photo', 'k25': 'image/K25', 'kdc': 'image/KDC',
             'library-ms': 'application/windows-library+xml', 'lpcm': 'audio/l16', 'lst': 'text/plain',
             'm2t': 'video/vnddlnampeg-tts', 'm2ts': 'video/vnddlnampeg-tts', 'm2v': 'video/mpeg',
             'm4a': 'audio/mp4', 'm4v': 'video/mp4', 'mak': 'text/plain', 'map': 'text/plain',
             'mcm': 'chemical/macromodel-input', 'mdp': 'text/plain', 'mef': 'image/MEF', 'mid': 'audio/mid',
             'midi': 'audio/mid', 'mk': 'text/plain', 'mka': 'audio/x-matroska', 'mkv': 'video/x-matroska',
             'mod': 'video/mpeg', 'mol': 'chemical/mdl-molfile', 'mop': 'chemical/x-mopac-input',
             'mos': 'image/MOS', 'mp2v': 'video/mpeg', 'mp4v': 'video/mp4', 'mpv2': 'video/mpeg',
             'mrw': 'image/MRW', 'msepub': 'application/epub+zip', 'msm': 'chemical/msimolfile',
             'mts': 'video/vnddlnampeg-tts', 'mtx': 'application/xml', 'natvis': 'text/xml', 'nef': 'image/NEF',
             'nrw': 'image/NRW', 'odc': 'text/x-ms-odc', 'odh': 'text/plain', 'odl': 'text/plain',
             'odp': 'application/vndoasisopendocumentpresentation',
             'ods': 'application/vndoasisopendocumentspreadsheet',
             'odt': 'application/vndoasisopendocumenttext', 'oga': 'audio/ogg', 'ogg': 'audio/ogg',
             'ogm': 'video/ogg', 'ogv': 'video/ogg', 'ogx': 'video/ogg', 'one': 'application/msonenote',
             'onepkg': 'application/msonenote', 'opus': 'audio/ogg', 'orderedtest': 'application/xml',
             'orf': 'image/ORF', 'ori': 'image/CR3', 'osdx': 'application/opensearchdescription+xml',
             'p10': 'application/pkcs10', 'p7b': 'application/x-pkcs7-certificates', 'p7m': 'application/pkcs7-mime',
             'p7r': 'application/x-pkcs7-certreqresp', 'p7s': 'application/pkcs7-signature',
             'pano': 'application/vndms-pano', 'pdfxml': 'application/vndadobepdfxml',
             'pdx': 'application/vndadobepdx', 'pef': 'image/PEF', 'pko': 'application/vndms-pkipko',
             'potm': 'application/vndms-powerpointtemplatemacroEnabled12',
             'potx': 'application/vndopenxmlformats-officedocumentpresentationmltemplate',
             'ppam': 'application/vndms-powerpointaddinmacroEnabled12',
             'ppsm': 'application/vndms-powerpointslideshowmacroEnabled12',
             'ppsx': 'application/vndopenxmlformats-officedocumentpresentationmlslideshow',
             'pptm': 'application/vndms-powerpointpresentationmacroEnabled12',
             'pptx': 'application/vndopenxmlformats-officedocumentpresentationmlpresentation',
             'prf': 'application/pics-rules', 'props': 'application/xml', 'psc1': 'application/PowerShell',
             'psh': 'text/plain', 'pshader': 'text/plain', 'ptx': 'image/PTX', 'pxn': 'image/PXN',
             'pyw': 'text/x-python', 'pyz': 'application/x-zip-compressed', 'pyzw': 'application/x-zip-compressed',
             'raf': 'image/RAF', 'rat': 'application/rat-file', 'raw': 'image/RAW', 'rc': 'text/plain',
             'rc2': 'text/plain', 'rct': 'text/plain', 'res': 'text/plain', 'resx': 'application/xml',
             'rgs': 'text/plain', 'rmi': 'audio/mid', 'rqy': 'text/x-ms-rqy', 'rtf': 'application/msword',
             'rw2': 'image/RW2', 'rwl': 'image/RWL', 's': 'text/plain', 'sct': 'text/scriptlet',
             'searchConnector-ms': 'application/windows-search-connector+xml', 'settings': 'application/xml',
             'shtml': 'text/html', 'sit': 'application/x-stuffit', 'sitemap': 'application/xml',
             'sldm': 'application/vndms-powerpointslidemacroEnabled12',
             'sldx': 'application/vndopenxmlformats-officedocumentpresentationmlslide',
             'slk': 'application/vndms-excel', 'sm2': 'x-sybylmol2', 'sml': 'x-sybylmol',
             'snippet': 'application/xml', 'spc': 'application/x-pkcs7-certificates', 'sr2': 'image/SR2',
             'srf': 'text/plain', 'srw': 'image/SRW', 'sst': 'application/vndms-pkicertstore',
             'targets': 'application/xml', 'testrunconfig': 'application/xml', 'testsettings': 'application/xml',
             'tgz': 'application/x-compressed', 'thmx': 'application/vndms-officetheme', 'tlh': 'text/plain',
             'tli': 'text/plain', 'tod': 'video/mpeg', 'trx': 'application/xml', 'ts': 'video/vnddlnampeg-tts',
             'tt': 'text/plain', 'tts': 'video/vnddlnampeg-tts', 'uitest': 'application/xml',
             'user': 'text/plain', 'uvu': 'video/vnddecemp4', 'vb': 'text/plain', 'vbproj': 'application/xml',
             'vcp': 'text/plain', 'vcproj': 'Application/xml', 'vcw': 'text/plain', 'vcxitems': 'Application/xml',
             'vcxproj': 'Application/xml', 'vdw': 'application/vndms-visioviewer',
             'vdx': 'application/vndms-visioviewer', 'vsd': 'application/vndms-visioviewer',
             'vsdm': 'application/vndms-visioviewer', 'vsdx': 'application/vndms-visioviewer',
             'vsh': 'text/plain', 'vshader': 'text/plain', 'vsmdi': 'application/xml', 'vsprops': 'Application/xml',
             'vss': 'application/vndms-visioviewer', 'vssettings': 'text/xml',
             'vssm': 'application/vndms-visioviewer', 'vssx': 'application/vndms-visioviewer',
             'vst': 'application/vndms-visioviewer', 'vstemplate': 'text/xml',
             'vstm': 'application/vndms-visioviewer', 'vsto': 'application/x-ms-vsto',
             'vstx': 'application/vndms-visioviewer', 'vsx': 'application/vndms-visioviewer',
             'vtx': 'application/vndms-visioviewer', 'wax': 'audio/x-ms-wax', 'wbk': 'application/msword',
             'wdp': 'image/vndms-photo', 'weba': 'audio/webm', 'website': 'application/x-mswebsite',
             'wm': 'video/x-ms-wm', 'wma': 'audio/x-ms-wma', 'WMD': 'application/x-ms-wmd', 'wmf': 'image/x-wmf',
             'wmv': 'video/x-ms-wmv', 'wmx': 'video/x-ms-wmx', 'wmz': 'application/x-ms-wmz',
             'wpl': 'application/vndms-wpl', 'wsc': 'text/scriptlet', 'wvx': 'video/x-ms-wvx', 'x3f': 'image/X3F',
             'xaml': 'application/xaml+xml', 'xbap': 'application/x-ms-xbap', 'xdp': 'application/vndadobexdp+xml',
             'xdr': 'application/xml', 'xfdf': 'application/vndadobexfdf', 'xht': 'application/xhtml+xml',
             'xhtml': 'application/xhtml+xml', 'xla': 'application/vndms-excel',
             'xlam': 'application/vndms-exceladdinmacroEnabled12', 'xld': 'application/vndms-excel',
             'xlk': 'application/vndms-excel', 'xll': 'application/vndms-excel', 'xlm': 'application/vndms-excel',
             'xlsb': 'application/vndms-excelsheetbinarymacroEnabled12',
             'xlsm': 'application/vndms-excelsheetmacroEnabled12',
             'xlsx': 'application/vndopenxmlformats-officedocumentspreadsheetmlsheet',
             'xlt': 'application/vndms-excel', 'xltm': 'application/vndms-exceltemplatemacroEnabled12',
             'xltx': 'application/vndopenxmlformats-officedocumentspreadsheetmltemplate',
             'xlw': 'application/vndms-excel', 'xps': 'application/vndms-xpsdocument', 'xrm-ms': 'text/xml',
             'xsc': 'application/xml', 'xsd': 'application/xml', 'xslt': 'application/xml',
             'xss': 'application/xml', 'z': 'application/x-compress', 'zmt': 'chemical/mopac-zmatrix'}

LANGUAGE = "language"
WEB_URL = "web_url"
DATE_RANGE = 'date_range'

MIME_TYPE_APPLICATION_JSON = "application/json"
FALLBACK_MESSAGE_PATTERN = '⁂'


EMAIL_REGEX = r"(^([^\s@]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})$)"
PHONE_REGEX = r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3,4})?[-. )]*(\d{3,4})?[-. ]*(\d{4,6})(?: *x(\d+))?\s*$'
VISITOR_CONTACT_CREATED_BY_VARIABLE = '¿·$user.info.contact_created_by·?'
PREVENT_VARIABLES_TO_UPDATE = [VISITOR_CONTACT_CREATED_BY_VARIABLE]


# cloud media upload constants

CHANNEL_PROVIDER_ID = 'channel_provider_id'
CHANNEL_CONFIGURATION_ID = 'channel_configuration_id'
TEMPLATE_ID = 'template_id'
API_KEY = 'api_key'
D360_API_KEY = 'D360-API-KEY'
AUTH_DETAILS = 'auth_details'
CONFIGURATIONS = 'configurations'
WHATSAPP_BUSINESS_ACCOUNT_ID = 'whatsapp_business_account_id'
CONTENT_TYPE = "Content-Type"
CONFIGURATION = 'configuration'
EXTRA = 'extra'
TOKEN = 'token'
PHONE_NUMBER_ID = 'phone_number_id'
AUTHORIZATION = 'Authorization'
ID = 'id'
MEDIA = 'media'
FILE = 'file'
BEARER = 'Bearer {}'
MEDIA_IS_NOT_DOWNLOAD = 'MEDIA_IS_NOT_DOWNLOAD'
SYSTEM_VARIABLE_FORMAT = "¿·$user.{variable_name}·?"
