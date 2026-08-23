import re

file_path = r"d:\ADP\ADPilot_Pro\scripts\build_executive_presentation.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update add_header_footer with Cyber Grid
old_header_start = """    def add_header_footer(slide, category_text, slide_title, subtitle_text, slide_num, total_slides=28):
        # 1. Background Canvas
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()"""

new_header_start = """    def add_header_footer(slide, category_text, slide_title, subtitle_text, slide_num, total_slides=28):
        # 1. Background Canvas
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()

        # Cyber Grid Background
        for i in range(1, 14):
            line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(i), 0, Inches(0.01), Inches(7.5))
            line.fill.solid()
            line.fill.fore_color.rgb = RGBColor(15, 23, 42)
            line.line.fill.background()
        for i in range(1, 8):
            line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(i), Inches(13.333), Inches(0.01))
            line.fill.solid()
            line.fill.fore_color.rgb = RGBColor(15, 23, 42)
            line.line.fill.background()"""
content = content.replace(old_header_start, new_header_start)

# 2. Update draw_card with HUD Accents
old_draw_card = """    def draw_card(slide, left, top, width, height, title="", border_color=None, bg_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color or BG_CARD
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.75)  # Thicker borders for bolder design
        else:
            card.line.color.rgb = RGBColor(40, 50, 70)
            card.line.width = Pt(1.0)

        if title:
            title_box = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(0.35))
            tf = title_box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title.upper()
            p.font.name = FONT_MONO
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = border_color or CYAN_PRIMARY
        return card"""

new_draw_card = """    def draw_card(slide, left, top, width, height, title="", border_color=None, bg_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color or BG_CARD
        card.line.color.rgb = RGBColor(30, 41, 59)
        card.line.width = Pt(1.0)

        if border_color:
            # HUD Cyber Accents (Top & Left)
            accent_top = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.06))
            accent_top.fill.solid()
            accent_top.fill.fore_color.rgb = border_color
            accent_top.line.fill.background()
            
            accent_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(0.06), Inches(height))
            accent_left.fill.solid()
            accent_left.fill.fore_color.rgb = border_color
            accent_left.line.fill.background()

        if title:
            title_box = slide.shapes.add_textbox(Inches(left + 0.3), Inches(top + 0.2), Inches(width - 0.5), Inches(0.35))
            tf = title_box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title.upper()
            p.font.name = FONT_MONO
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = border_color or CYAN_PRIMARY
        return card"""
content = content.replace(old_draw_card, new_draw_card)

# 3. Update embed_framed_image with HUD Accents
old_embed = """    def embed_framed_image(slide, left, top, width, height, image_path, caption=None, border_color=CYAN_PRIMARY):
        if image_path and os.path.exists(image_path):
            # Frame card
            frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
            frame.fill.solid()
            frame.fill.fore_color.rgb = BG_CARD
            frame.line.color.rgb = border_color
            frame.line.width = Pt(1.75)

            # Insert Image
            img_margin = 0.15
            slide.shapes.add_picture(
                image_path,
                Inches(left + img_margin),
                Inches(top + img_margin),
                Inches(width - 2 * img_margin),
                Inches(height - (0.45 if caption else 2 * img_margin))
            )"""

new_embed = """    def embed_framed_image(slide, left, top, width, height, image_path, caption=None, border_color=CYAN_PRIMARY):
        if image_path and os.path.exists(image_path):
            # Frame card
            frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
            frame.fill.solid()
            frame.fill.fore_color.rgb = BG_CARD
            frame.line.color.rgb = RGBColor(30, 41, 59)
            frame.line.width = Pt(1.0)

            # HUD Cyber Accents (Top & Left)
            accent_top = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.06))
            accent_top.fill.solid()
            accent_top.fill.fore_color.rgb = border_color
            accent_top.line.fill.background()
            
            accent_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(0.06), Inches(height))
            accent_left.fill.solid()
            accent_left.fill.fore_color.rgb = border_color
            accent_left.line.fill.background()

            # Insert Image
            img_margin = 0.15
            slide.shapes.add_picture(
                image_path,
                Inches(left + img_margin),
                Inches(top + img_margin),
                Inches(width - 2 * img_margin),
                Inches(height - (0.45 if caption else 2 * img_margin))
            )"""
content = content.replace(old_embed, new_embed)

# 4. Enhance text coordinates slightly since left accent adds 0.06 inches
content = re.sub(r'c_left \+ 0\.25\)', 'c_left + 0.3)', content)
content = re.sub(r'cl \+ 0\.25\)', 'cl + 0.3)', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied premium cyber-design HUD accents and grid background!")
