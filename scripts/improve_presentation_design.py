import re

file_path = r"d:\ADP\ADPilot_Pro\scripts\build_executive_presentation.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update draw_card
old_draw_card = """    def draw_card(slide, left, top, width, height, title="", border_color=None, bg_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color or BG_CARD
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.2)
        else:
            card.line.color.rgb = RGBColor(30, 41, 59)
            card.line.width = Pt(0.8)

        if title:
            title_box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.12), Inches(width - 0.3), Inches(0.3))
            tf = title_box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title.upper()
            p.font.name = FONT_MONO
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = border_color or CYAN_PRIMARY
        return card"""

new_draw_card = """    def draw_card(slide, left, top, width, height, title="", border_color=None, bg_color=None):
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
content = content.replace(old_draw_card, new_draw_card)

# 2. Update embed_framed_image
old_embed = """    def embed_framed_image(slide, left, top, width, height, image_path, caption=None, border_color=CYAN_PRIMARY):
        if image_path and os.path.exists(image_path):
            # Frame card
            frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
            frame.fill.solid()
            frame.fill.fore_color.rgb = BG_CARD
            frame.line.color.rgb = border_color
            frame.line.width = Pt(1.2)

            # Insert Image
            img_margin = 0.08
            slide.shapes.add_picture(
                image_path,
                Inches(left + img_margin),
                Inches(top + img_margin),
                Inches(width - 2 * img_margin),
                Inches(height - (0.35 if caption else 2 * img_margin))
            )

            # Optional caption bar
            if caption:
                cbox = slide.shapes.add_textbox(Inches(left + 0.1), Inches(top + height - 0.32), Inches(width - 0.2), Inches(0.28))
                tf = cbox.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                p.text = caption.upper()
                p.font.name = FONT_MONO
                p.font.size = Pt(8)
                p.font.bold = True
                p.font.color.rgb = border_color"""

new_embed = """    def embed_framed_image(slide, left, top, width, height, image_path, caption=None, border_color=CYAN_PRIMARY):
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
            )

            # Optional caption bar
            if caption:
                cbox = slide.shapes.add_textbox(Inches(left + 0.1), Inches(top + height - 0.4), Inches(width - 0.2), Inches(0.35))
                tf = cbox.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                p.text = caption.upper()
                p.font.name = FONT_MONO
                p.font.size = Pt(9)
                p.font.bold = True
                p.font.color.rgb = border_color"""
content = content.replace(old_embed, new_embed)

# 3. Increase offsets for textboxes to improve margins
content = re.sub(r'c_left \+ 0\.12', 'c_left + 0.25', content)
content = re.sub(r'c_left \+ 0\.15', 'c_left + 0.25', content)
content = re.sub(r'c_left \+ 0\.2\)', 'c_left + 0.25)', content)

content = re.sub(r'cl \+ 0\.12', 'cl + 0.25', content)
content = re.sub(r'cl \+ 0\.15', 'cl + 0.25', content)

content = re.sub(r'c_top \+ 0\.38', 'c_top + 0.5', content)
content = re.sub(r'ct \+ 0\.38', 'ct + 0.5', content)
content = re.sub(r'ct \+ 0\.4\)', 'ct + 0.5)', content)
content = re.sub(r'ct \+ 0\.42', 'ct + 0.55', content)

# Slightly reduce width/height of internal textboxes to account for higher left/top margins
content = re.sub(r'Inches\(2\.48\)', 'Inches(2.28)', content)
content = re.sub(r'Inches\(2\.5\)', 'Inches(2.3)', content)
content = re.sub(r'Inches\(3\.35\)', 'Inches(3.25)', content)
content = re.sub(r'Inches\(5\.35\)', 'Inches(5.25)', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated script design margins successfully!")
