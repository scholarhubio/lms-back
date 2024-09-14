"""# CKEditor Settings

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 

# CKEditor UI and plugins configuration
CKEDITOR_CONFIGS = {
    'default': {
        # Toolbar configuration
        # name - Toolbar name
        # items - The buttons enabled in the toolbar
        'toolbar_DefaultToolbarConfig': [
            {
                'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                          'Superscript', ],
            },
            {
                'name': 'clipboard',
                'items': ['Undo', 'Redo', ],
            },
            {
                'name': 'paragraph',
                'items': ['NumberedList', 'BulletedList', 'Outdent', 'Indent',
                          'HorizontalRule', 'JustifyLeft', 'JustifyCenter',
                          'JustifyRight', 'JustifyBlock', ],
            },
            {
                'name': 'format',
                'items': ['Format', ],
            },
            {
                'name': 'extra',
                'items': ['Link', 'Unlink', 'Blockquote', 'Image', 'Table',
                          'CodeSnippet', 'Mathjax', 'Embed', ],
            },
            {
                'name': 'source',
                'items': ['Maximize', 'Source', ],
            },
        ],

        # This hides the default title provided by CKEditor
        'title': False,

        # Use this toolbar
        'toolbar': 'DefaultToolbarConfig',

        # Which tags to allow in format tab
        'format_tags': 'p;h1;h2',

        # Remove these dialog tabs (semicolon separated dialog:tab)
        'removeDialogTabs': ';'.join([
            'image:advanced',
            'image:Link',
            'link:upload',
            'table:advanced',
            'tableProperties:advanced',
        ]),
        'linkShowTargetTab': False,
        'linkShowAdvancedTab': False,

        # CKEditor height and width settings
        'height': '250px',
        'width': 'auto',
        'forcePasteAsPlainText ': True,

        # Class used inside span to render mathematical formulae using latex
        'mathJaxClass': 'mathjax-latex',

        # Mathjax library link to be used to render mathematical formulae
        'mathJaxLib': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_SVG',

        # Tab = 4 spaces inside the editor
        'tabSpaces': 4,

        # Extra plugins to be used in the editor
        'extraPlugins': ','.join([
            # 'devtools',  # Shows a tooltip in dialog boxes for developers
            'mathjax',  # Used to render mathematical formulae
            'codesnippet',  # Used to add code snippets
            'image2',  # Loads new and better image dialog
            'embed',  # Used for embedding media (YouTube/Slideshare etc)
            'tableresize',  # Used to allow resizing of columns in tables
        ]),
    }
}"""


# settings.py or components/ckeditor.py

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join([
            'mathjax',
            'codesnippet',
            'image2',
            'embed',
            'tableresize',
        ]),
        'removePlugins': 'uploadimage,uploadwidget,uploadfile,filetools,filebrowser',
        'height': '250px',
        'width': 'auto',
        'forcePasteAsPlainText': True,

        # Define the toolbar configuration
        'toolbar_DefaultToolbarConfig': [
            {
                'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            },
            {
                'name': 'clipboard',
                'items': ['Undo', 'Redo'],
            },
            {
                'name': 'paragraph',
                'items': ['NumberedList', 'BulletedList', 'Outdent', 'Indent', 'HorizontalRule', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            },
            {
                'name': 'format',
                'items': ['Format'],
            },
            {
                'name': 'extra',
                'items': ['Link', 'Unlink', 'Blockquote', 'Image', 'Table', 'CodeSnippet', 'Mathjax', 'Embed', 'ckeditor_wiris'],  # Ensure ckeditor_wiris is here
            },
            {
                'name': 'source',
                'items': ['Maximize', 'Source'],
            },
        ],
        'specialChars': [
            '!','@','#','$','%','^','&','*','(',')','_','+',
            '√', '∑', '∞', 'π', '∫', 'Δ', 'Ω', '±', '÷', '×',
            '≈', '≠', '≤', '≥', '∂', '∇', '∏', '∝', '⊗',
            '◊', '□', '■', '●', '○', '■', '▲', '▼',
            '↔', '↕', '⇒', '⇔', '⇑', '⇓', '→', '←',
        ],
    },
}
