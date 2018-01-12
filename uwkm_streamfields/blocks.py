from django.conf import settings

from django import forms
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from .icons import IconChoiceBlock
from .widgets import ColorPickerWidget

TABLE_OPTIONS = {
    'minSpareRows': 0,
    'startRows': 4,
    'startCols': 4,
    'colHeaders': False,
    'rowHeaders': False,
    'contextMenu': True,
    'editor': 'text',
    'stretchH': 'all',
    'height': 108,
    'language': 'nl',
    'renderer': 'text',
    'autoColumnSize': False,
}



class ColorPickerBlock(blocks.FieldBlock):
    def __init__(self, required=True, **kwargs):
        self.field = forms.CharField(required=required, widget=ColorPickerWidget)
        super(ColorPickerBlock, self).__init__(**kwargs)


class AlignChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ]


class GridChoiceBlock(blocks.ChoiceBlock):
    BS_SIZE = settings.BS_SIZE
    choices = [
        ('col-%s-12' % BS_SIZE, '12'),
        ('col-%s-11' % BS_SIZE, '11'),
        ('col-%s-10' % BS_SIZE, '10'),
        ('col-%s-9' % BS_SIZE, '9'),
        ('col-%s-8' % BS_SIZE, '8'),
        ('col-%s-7' % BS_SIZE, '7'),
        ('col-%s-6' % BS_SIZE, '6'),
        ('col-%s-5' % BS_SIZE, '5'),
        ('col-%s-4' % BS_SIZE, '4'),
        ('col-%s-3' % BS_SIZE, '3'),
        ('col-%s-2' % BS_SIZE, '2'),
        ('col-%s-1' % BS_SIZE, '1'),
    ]


class MasonryGalleryBlock(blocks.StructBlock):
    columns = blocks.ChoiceBlock(
        label = _('Columns'),
        default = '4',
        choices = (
            ('2', '2 column'),
            ('3', '3 column'),
            ('4', '4 column'),
            ('5', '5 column'),
            ('6', '6 column'),
        )
    )
    big_img = blocks.IntegerBlock(
        label = _('Large image'),
        required = False,
        help_text = 'Optional: how many pictures (from the pictures below) will be a "big picture".'
    )
    image = blocks.ListBlock(
        ImageChooserBlock(),
        icon='image',
        label=_('Image'),
    )


class SliderBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    name = blocks.CharBlock(
        label=_('Name'),
        max_length = 30,
        help_text = _('Appears below as navigation button.'),
        required = True,
    )

    subtext = blocks.CharBlock(
        label=_('Subtext'),
        max_length = 35,
        help_text = _('Appears under the navigation button.'),
        required = False,
    )

    button = blocks.BooleanBlock(
        label='Call to Action',
        default=False,
        help_text = _('Has a call to action button.'),
        required = False,
    )

    cta_text = blocks.CharBlock(
        label=_('CTA text'),
        max_length = 20,
        required = False,
    )

    cta_pos  = blocks.ChoiceBlock(
        label = _('CTA Position'),
        choices = (
            ('left', 'Left'),
            ('right', 'Right')
        ),
        required = False,
    )

    # cta_color_picker = ColorPickerBlock(
    #     label = _('CTA background color selector'),
    #     required = False,
    # )

    cta_link_type = blocks.ChoiceBlock(
        label = 'CTA link type',
        choices = (
            ('wagtail', 'Wagtail page'),
            ('url', 'Manual url')
        ),
        required = False,
    )

    cta_page_link = blocks.PageChooserBlock(
        label = 'CTA wagtail link',
        can_choose_root = True,
        required= False,
    )

    cta_url = blocks.CharBlock(
        label='CTA url',
        max_length = 255,
        required = False,
    )

    class Meta:
        icon = 'image'


class SloganBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    title = blocks.CharBlock(
        label = _('Name'),
        max_length = 30,
        help_text = _('Appears below as navigation button.'),
        required = True,
    )

    text = blocks.TextBlock(
        label = _('Text'),
        max_length = 120,
    )


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(
        label = _('Quote'),
        required = True,
        max_length = 150,
    )

    quote_pos = blocks.ChoiceBlock(
        choices = (
            ('up', 'Above'),
            ('under', 'Under'),
        ),
        label = _('Position quote'),
        help_text = _('The position of the quote (above or below the picture).',)
    )

    quote_size = blocks.ChoiceBlock(
        choices = (
            ('24px', '24px'),
            ('40px', '40px'),
        ),
        label = _('Quote text size'),
        help_text = _('The text size of the quote.'),
    )

    # quote_background_color = ColorPickerBlock(
    #     label = _('Background color'),
    #     required = False,
    #     help_text = _('The background color of the quote.')
    # )

    # quote_color = ColorPickerBlock(
    #     label = 'Color text',
    #     required = False,
    #     help_text = 'The text color of the quote.'
    # )

    logo = ImageChooserBlock(required = False)

    name = blocks.CharBlock(
        label = _('Name'),
        max_length = 50,
        help_text = _('Name of the person behind the quote.'),
    )

    company = blocks.CharBlock(
        label = _('Company'),
        max_length = 50,
        help_text = _('Name of the company behind the quote.'),
    )

    city = blocks.CharBlock(
        label = _('Place'),
        max_length = 50,
        help_text = _('Place'),
    )

    link = blocks.PageChooserBlock(
        label = _('Internal link'),
        can_choose_root = True,
        required = False,
    )


class HeaderChoiceBlock(blocks.ChoiceBlock):
    choices = (
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
    )


class HeaderBlock(blocks.StructBlock):
    header = HeaderChoiceBlock(
        label = _('Head size'),
        help_text = _('Size of the text.')
    )

    text = blocks.CharBlock(
        label = _('Text'),
        max_length = 50,
        help_text = _('Text of the header.'),
    )


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label = _('Title'),
        max_length = 50,
        help_text = _('Text in the title.'),
    )

    content = blocks.RichTextBlock(
        label = _('Content'),
        help_text = _('Contents of the tab.'),
    )


class TabBlock(blocks.StructBlock):
    icon = IconChoiceBlock(
        label = 'Icon',
        help_text = 'Icon. (Font awesome)',
        required = False,
    )
    title = blocks.CharBlock(
        label = _('Title'),
        max_length = 50,
        help_text = _('Text in the title.'),
    )
    content = blocks.RichTextBlock(
        label = 'Content',
        help_text = _('Contents of the tab.'),
    )


class UnorderedListBlock(blocks.StructBlock):
    bullet_icon = ImageChooserBlock(
        label = _('Image icon'),
        help_text = _('The image icon per bullet.'),
        required=False,
    )
    content = blocks.ListBlock(
        blocks.RichTextBlock(),
        label = _('Bullets'),
        help_text = _('Content of the bullet.'),
    )


class TextFieldBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(
        label = _('Text box'),
        help_text = _('Content of the text field.'),
    )


# class InfoBoxBlock(blocks.StructBlock):
#     tekst = blocks.RichTextBlock()

#     class Meta:
#         template = 'streamfields/infoblock.html'

class BackgroundBlock(blocks.StructBlock):
    type_field = blocks.ChoiceBlock(
        choices=(
            ('parallaxBg', 'Parallax'),
            ('fixedBg', 'Stilstaand'),
        )
    )
    background_image = ImageChooserBlock(
        label = _('Image'),
        help_text = _('The background image of the block.'),
    )
    block_height = blocks.IntegerBlock(
        label = _('Height'),
        help_text = _('Height of the block in pixels.'),
        min_value = 0,
        max_value = 999,
        default = 250,
    )
    columns = blocks.ChoiceBlock(
        label = 'Columns',
        choices = [('2', 'Two'), ('1', 'One')],
        default = '2',
    )
    text_left = blocks.RichTextBlock(
        label = _('Text left'),
        help_text = 'Text on the left in the background.',
        required = False,
    )
    text_right = blocks.RichTextBlock(
        label = _('Text right'),
        help_text = 'Text on the right in the background.',
        required = False,
    )
    # text_color = ColorPickerBlock(
    #     label = _('Color text'),
    #     required = False,
    # )


class ColoredTextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(
        label = _('Text'),
        required = False,
    )
    # color = ColorPickerBlock(
    #     label = _('Color picker'),
    #     required = False,
    # )
    # bg_color = ColorPickerBlock(
    #     label = _('Background color picker'),
    #     required = False,
    # )


class DividerBlock(blocks.StructBlock):
    # border_color = ColorPickerBlock(
    #     label = _('Divider'),
    #     help_text = 'Line color.',
    # )
    border_width = blocks.IntegerBlock(
        label=_("Thckness"),
        default=2,
        min_value=1,
        max_value=50,
        help_text="The thickness of the horizontal line.",
    )


class HTMLBlock(blocks.StructBlock):
    raw_html = blocks.RawHTMLBlock(
        label = _('HTML block'),
        help_text = 'HTML block',
    )


class ButtonBlock(blocks.StructBlock):
    # button_color = ColorPickerBlock(
    #     label = _('Background color picker'),
    #     help_text = 'The color of the background.',
    #     required = False,
    # )
    # color = ColorPickerBlock(
    #     label = _('Font color selector'),
    #     help_text = 'The color of the text.',
    #     required = False,
    # )
    icon = IconChoiceBlock(
        label = _('Icon'),
        help_text = 'Icon on the button.. (Font awesome)',
        required = False,
    )
    icon_size = blocks.IntegerBlock(
        label = _('Icon size'),
        help_text = 'Size of the icon on the button. (in pixels)',
        default = 14,
    )
    text = blocks.CharBlock(
        label = _('Text'),
        max_length = 50,
        help_text = 'Tekst op de knop.',
    )
    text_size = blocks.IntegerBlock(
        label = _('Text Size'),
        help_text = 'Size of the text on the button. (in pixels)',
        default = 14,
    )
    width = blocks.ChoiceBlock(
        label = _('Width'),
        choices = [
            (' ', 'Automatically'), ('btn-block', '100%'),
        ]
    )
    link = blocks.PageChooserBlock(
        label = _('Link'),
        can_choose_root = True,
        required= False,
        help_text="Choose one of the two: link / external link."
    )
    ext_link = blocks.CharBlock(
        label='Externe link',
        max_length = 255,
        required = False,
        help_text="Choose one of the two: link / external link."
    )


class VideoBlock(blocks.StructBlock):
    video_id = blocks.CharBlock(
        label = _('Video'),
        max_length = 11,
        help_text = 'YouTube video code/id.',
    )


class IconBlock(blocks.StructBlock):
    align = AlignChoiceBlock(
        label = _('Alignment'),
        help_text = 'Alignment of the text.'
    )
    icon = IconChoiceBlock(
        label = _('Icon'),
        help_text = 'Icon. (Font awesome)',
    )
    text = blocks.RichTextBlock(
        label = _('Text'),
        help_text = 'Text in the block.',
    )


class CallToActionBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(
        label = _('Text'),
        help_text = 'Text in the block.',
    )
    button = ButtonBlock()


class TableStructBlock(blocks.StructBlock):
    type_table = blocks.ChoiceBlock(
        choices = [(' ', 'Ordinary table'), ('price-table', 'Price table')],
        label=_('Type table'),
    )
    table_borders = blocks.ChoiceBlock(
        choices = [
            ('no-borders', 'No lines'), ('column-borders', 'Column lines'),
            ('row-borders', 'Now lines'), ('all-borders', 'Column and line lines'),
        ],
        label=_('Table lines')
    )
    table_header_rows = blocks.IntegerBlock(
        label = _('Table header'),
        min_value = 0,
        max_value = 100,
        default = 2,
    )
    table_footer_rows = blocks.IntegerBlock(
        label = _('Table footer'),
        min_value = 0,
        max_value = 100,
        default = 2,
    )
    # table_header_background = ColorPickerBlock(
    #     label = _('Table header background'),
    #     required = False,
    # )
    # table_header_color = ColorPickerBlock(
    #     label = _('Table header color'),
    #     required = False,
    # )
    table_header_text_size = blocks.IntegerBlock(
        label = _('Table header size text'),
        help_text = 'Table header size of the text.',
        min_value = 1,
        max_value = 100,
        default = 20,
    )
    # table_footer_background = ColorPickerBlock(
    #     label = _('Table footer background color'),
    #     required = False,
    # )
    # table_footer_color = ColorPickerBlock(
    #     label = _('Table footer color'),
    #     required = False,
    # )
    table = TableBlock(
        label=_('Tabel'),
        table_options=TABLE_OPTIONS,
        help_text='HTML is possible in the table'
    )


class ActionBlock(blocks.StructBlock):
    action = blocks.CharBlock(
        verbose_name="Action",
        help_text="Text that appears at the top left of the image. For example: Blog"
    )
    # color = ColorPickerBlock(
    #     label = _('Background color'),
    #     help_text='Background color for action',
    #     required = False,
    # )
    image = ImageChooserBlock()
    date = blocks.DateBlock(
        required=False,
        help_text="Optional. For example for blogs or special events."
    )
    title = blocks.CharBlock(
        verbose_name=_("Title"),
        help_text="Title of your action block. Example: Review: The new HP Latex 570"
    )
    link = blocks.CharBlock(
        verbose_name="Link url",
        help_text="Enter a url manually here. For example: / contact / or www.google.nl"
    )
    link_text = blocks.CharBlock(
        verbose_name="Link text", help_text="Enter a url text manually here. For example: view all blog articles or view all reviews."
    )


class LogoBlock(blocks.StructBlock):
    link = blocks.PageChooserBlock()
    icon = ImageChooserBlock()
    title = blocks.CharBlock(blank=True,default='')
    image = ImageChooserBlock()


class DownloadLinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(blank=True,default='')
    buttontext = blocks.CharBlock(blank=True,default='')
    link = DocumentChooserBlock()
    image = ImageChooserBlock()


class RevSliderBlock(blocks.StructBlock):
    image = ImageChooserBlock()


class OwlGalleryBlock(blocks.StructBlock):
    image = ImageChooserBlock()


class CoworkerBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255,blank=True)
    roepnaam = blocks.CharBlock(max_length=255, null=True,blank=True)
    job_function = blocks.CharBlock(max_length=255, blank=True, null=True)
    address = blocks.CharBlock(max_length=255, blank=True, null=True, required=False,)
    email = blocks.EmailBlock(max_length=254, blank=True, null=True, required=False,)
    phone = blocks.CharBlock(max_length=255, blank=True, null=True, required=False,)
    linkedin = blocks.URLBlock(max_length=200, blank=True, null=True, required=False,)
    positions = blocks.IntegerBlock(default=1)
    image = ImageChooserBlock()


class ProjectBlock(blocks.StructBlock):
    title = blocks.CharBlock(blank=True,default='')
    image = ImageChooserBlock()
    link = blocks.PageChooserBlock()


class GoogleMapsBlock(blocks.StructBlock):
    address = blocks.TextBlock(
        label = _('Address'),
        help_text = 'Address, place, country',
        required = False,
    )
    height = blocks.IntegerBlock(
        label = _('Height'),
        help_text = 'Height of the block in pixels.',
        min_value = 0,
        max_value = 999,
        default = 250,
    )


grid_array = \
    [('tables', TableStructBlock(
        label=_('Tables'),
        template = 'streamfields/table.html',
        icon='fa-table'))
    ,('quotes', blocks.ListBlock(
        QuoteBlock(),
        label=_('Quotes'),
        template = 'streamfields/quotes.html',
        icon="openquote",))
    ,('heads', blocks.ListBlock(
        HeaderBlock(),
        label=_('Heads'),
        template = 'streamfields/header.html',
        icon="title",))
    ,('text_fields', blocks.ListBlock(
        TextFieldBlock(),
        label=_('Text fields'),
        template = 'streamfields/text_field.html',
        icon="fa-align-justify",))
    ,('list', blocks.ListBlock(
        UnorderedListBlock(),
        label=_('List'),
        template = 'streamfields/list.html',
        icon="list-ul"))
    ,('accordions', blocks.ListBlock(
        AccordionBlock(),
        label=_('accordions'),
        template = 'streamfields/accordion.html',
        icon='list-ol',))
    ,('tabs', blocks.ListBlock(
        TabBlock(),
        label=_('Tabs'),
        template = 'streamfields/tab.html',
        icon='list-ol',))
    ,('verticale_tabs', blocks.ListBlock(
        TabBlock(),
        label=_('Verticale tabs'),
        template = 'streamfields/vertical_tab.html',
        icon='list-ol',))
    ,('image_with_text', blocks.ListBlock(
        BackgroundBlock(),
        label=_('Image with text'),
        template = 'streamfields/background_with_text.html',
        icon='doc-full',))
    ,('colored_blocks', blocks.ListBlock(
        ColoredTextBlock(),
        label=_('Colored blocks'),
        template = 'streamfields/colored_block.html',
        icon="doc-full-inverse",))
    ,('masonry_gallery', blocks.ListBlock(
        MasonryGalleryBlock(),
        label=_('masonry gallery'),
        template = 'streamfields/masonry_gallery.html',
        icon='fa-th',))
    ,('owl_gallery', blocks.ListBlock(
        OwlGalleryBlock(),
        template = 'streamfields/owl_gallery.html',
        icon='image',))
    ,('image', ImageChooserBlock(
        template = 'streamfields/image.html',
        label=_('Image'),
        icon='image'))
    ,('divider', blocks.ListBlock(
        DividerBlock(),
        label=_('Divider'),
        template = 'streamfields/divider.html',
        icon="horizontalrule",))
    ,('html', blocks.ListBlock(
        HTMLBlock(),
        label=_('Html'),
        template = 'streamfields/raw_html.html',
        icon="code",))
    ,('button', blocks.ListBlock(
        ButtonBlock(),
        label=_('Button'),
        template = 'streamfields/button.html',
        icon="fa-hand-pointer-o",))
    ,('video', blocks.ListBlock(
        VideoBlock(),
        label=_('Video'),
        template = 'streamfields/video.html',
        icon="media",))
    ,('icon', blocks.ListBlock(
        IconBlock(),
        label=_('Icon'),
        template = 'streamfields/icon_block.html',
        icon="fa-font-awesome",))
    ,('call_to_action', blocks.ListBlock(
        CallToActionBlock(),
        label=_('CallToAction'),
        template = 'streamfields/call_to_action.html',
        icon="fa-reply",))
    ,('tab_slider', blocks.ListBlock(
        SliderBlock(),
        label=_('Tab Slider'),
        template = 'streamfields/tab_slider.html',
        icon="image"))
    ,('action', blocks.ListBlock(
        ActionBlock(),
        label=_('Action'),
        template = 'streamfields/action.html',
        icon="fa-exclamation"))
    ,('logo_blocks', blocks.ListBlock(
        LogoBlock(),
        label=_('Logo Blocks'),
        template = 'streamfields/logo_block.html',
        icon="image"))
    ,('download_link', blocks.ListBlock(
        DownloadLinkBlock(),
        template = 'streamfields/download_link.html',
        icon='fa-download'))
    ,('rev_slider', blocks.ListBlock(
        RevSliderBlock(),
        template = 'streamfields/rev_slider.html',
        icon="image"))
    ,('collaborator', blocks.ListBlock(
        CoworkerBlock(),
        template = 'streamfields/coworker.html',
        icon="fa-user-plus"))
    ,('project', blocks.ListBlock(
        ProjectBlock(),
        template = 'streamfields/project.html',
        icon="fa-comments-o"))
    ,('google_maps', GoogleMapsBlock(
        template = 'streamfields/google_maps.html',
        icon='fa-map-o'))
    ,]

# Check if oscar_wagtail is in installed apps so they can access product streamfield
if 'oscar_wagtail' in settings.INSTALLED_APPS:
    from oscar.core.loading import get_model
    class ProductChooserBlock(blocks.ChooserBlock):
        @cached_property
        def target_model(self):
            return get_model('catalogue', 'Product')

        widget = forms.Select

        class Meta:
            app_label = 'catalogue'

        def value_for_form(self, value):
            # return the key value for the select field
            if isinstance(value, self.target_model):
                return value.pk
            else:
                return value


    class ProductBlock(blocks.StructBlock):
        products = blocks.ListBlock(ProductChooserBlock)

    grid_array.append(
        ('product', blocks.ListBlock(
            ProductBlock(),
            template = 'streamfields/product.html',
            icon="fa-shopping-cart")
        ),
    )

validated_grid_array = []
STREAMFIELDS = settings.STREAMFIELDS
EXCLUDE_STREAMFIELDS = settings.EXCLUDE_STREAMFIELDS

# validate streamfields
if STREAMFIELDS == '__all__':
    if len(EXCLUDE_STREAMFIELDS) > 0:
        for streamfield in grid_array:
            if streamfield[0] not in EXCLUDE_STREAMFIELDS:
                validated_grid_array.append(streamfield)
    else:
        validated_grid_array = grid_array
else:
    for streamfield in grid_array:
        if streamfield[0] in STREAMFIELDS:
            validated_grid_array.append(streamfield)


class GridBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=50,
        required=False,
        classname="grid-title"
    )
    grid = GridChoiceBlock(
        label = _('Width column'),
        help_text = _('The width columns (* / 12).'),
    )
    grid_classes = blocks.CharBlock(
        max_length=255,
        required=False,
        label = _('Classes'),
        help_text = _('The classes of the grid.'),
    )
    content = blocks.StreamBlock(
        validated_grid_array,
        label="Content"
    )

