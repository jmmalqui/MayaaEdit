from typing import Union
import pygame as pg


class Properties:
    align_object = None
    align_items = None
    align_self = None
    all = None
    animation_delay = None
    animation_direction = None
    animation_duration = None
    animation_fill_mode = None
    animation_iteration_count = None
    animation_name = None
    animation_play_state = None
    animation_timing_function = None
    backface_visibility = None
    background = None
    background_attachment = None
    background_blend_mode = None
    background_clip = None
    background_color = None
    background_image = None
    background_origin = None
    background_position = None
    background_repeat = None
    background_size = None
    border = None
    border_bottom = None
    border_bottom_color = None
    border_bottom_left_radius = None
    border_bottom_right_radius = None
    border_bottom_style = None
    border_bottom_width = None
    border_collapse = None
    border_color = None
    border_image = None
    border_image_outset = None
    border_image_repeat = None
    border_image_slice = None
    border_image_source = None
    border_image_width = None
    border_left = None
    border_left_color = None
    border_left_style = None
    border_left_width = None
    border_radius = None
    border_right = None
    border_right_color = None
    border_right_style = None
    border_right_width = None
    border_spacing = None
    border_style = None
    border_top = None
    border_top_color = None
    border_top_left_radius = None
    border_top_right_radius = None
    border_top_style = None
    border_top_width = None
    border_width = None
    bottom = None
    box_shadow = None
    box_sizing = None
    caption_side = None
    caret_color = None
    charset = None
    clear = None
    clip = None
    clip_path = None
    color = None
    column_count = None
    column_fill = None
    column_gap = None
    column_rule = None
    column_rule_color = None
    column_rule_style = None
    column_rule_width = None
    column_span = None
    column_width = None
    columns = None
    content = None
    counter_increment = None
    counter_reset = None
    cursor = None
    direction = None
    display = None
    empty_cells = None
    Filter = None
    flex = None
    flex_basis = None
    flex_direction = None
    flex_flow = None
    flex_grow = None
    flex_shrink = None
    flex_wrap = None
    Float = None
    font = None
    font_face = None
    font_family = None
    font_kerning = None
    font_size = None
    font_size_adjust = None
    font_stretch = None
    font_style = None
    font_variant = None
    font_weight = None
    grid = None
    grid_area = None
    grid_auto_columns = None
    grid_auto_flow = None
    grid_auto_rows = None
    grid_column = None
    grid_column_end = None
    grid_column_gap = None
    grid_column_start = None
    grid_gap = None
    grid_row = None
    grid_row_end = None
    grid_row_gap = None
    grid_row_start = None
    grid_template = None
    grid_template_areas = None
    grid_template_columns = None
    grid_template_rows = None
    height = None
    hyphens = None
    Import = None
    justify_content = None
    keyframes = None
    left = None
    letter_spacing = None
    line_height = None
    list_style = None
    list_style_image = None
    list_style_type = None
    margin = None
    margin_bottom = None
    margin_left = None
    margin_right = None
    margin_top = None
    max_height = None
    max_width = None
    media = None
    min_height = None
    min_width = None
    object_fit = None
    object_position = None
    opacity = None
    order = None
    outline = None
    outline_color = None
    outline_offset = None
    outline_style = None
    outline_width = None
    overflow = None
    overflow_x = None
    overflow_y = None
    padding = None
    padding_bottom = None
    padding_left = None
    padding_right = None
    padding_top = None
    page_break_after = None
    page_break_before = None
    page_break_inside = None
    perspective = None
    perspective_origin = None
    pointer_events = None
    position = None
    quotes = None
    right = None
    scroll_behavior = None
    table_layout = None
    text_align = None
    text_align_last = None
    text_decoration = None
    text_decoration_color = None
    text_decoration_line = None
    text_decoration_style = None
    text_indent = None
    text_justify = None
    text_overflow = None
    text_shadow = None
    text_transform = None
    top = None
    transform = None
    transform_origin = None
    transform_style = None
    transition = None
    transition_delay = None
    transition_duration = None
    transition_property = None
    transition_timing_function = None
    user_select = None
    vertical_align = None
    visibility = None
    white_space = None
    width = None
    word_break = None
    word_spacing = None
    word_wrap = None
    writing_mode = None
    z_index = None


class DefaultProperties(Properties):
    color = "black"
    font_size = 12
    background_color = None


class ContentLike(object):
    def __init__(self) -> None:
        pass


class Image(ContentLike):
    def __init__(self, source: Union[pg.Surface, str]) -> None:
        super().__init__()
        self.source = source


class Text(ContentLike):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text


class UIObjectSizeAllocator:
    def __init__(self, properties: Properties) -> None:
        if not properties:
            raise ValueError("Could not allocate size for UI Object")
        self.properties = properties
        self.margin = properties.margin
        self.padding = properties.padding

    def allocate(self) -> pg.Vector2:
        return pg.Vector2()


class UIObject:
    def __init__(
        self,
        master,
        properties: Properties = DefaultProperties,
        content: ContentLike = Text,
    ) -> None:
        self.master: UIObject = master
        self.ui_objects: list[UIObject] = []
        self.properties = properties
        self.content = content
        self.allocated_size = UIObjectSizeAllocator(self.properties).allocate()
        self.master.add_ui_object(self)

    def update(self):
        ...

    def render(self):
        ...
