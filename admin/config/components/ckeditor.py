CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'mathJaxLib': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
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
