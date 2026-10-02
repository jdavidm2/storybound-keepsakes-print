import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Storybound Keepsakes - Print Generator", layout="centered")

st.title("Storybound Keepsakes Print Generator")
st.write("Generate a printable 8.5x11 sheet of custom bookplates.")

with st.form("generator_form"):
    reader_name = st.text_input("Reader's Name (e.g., Grandpa Jim)", "")
    audio_url = st.text_input("Cloudflare Audio URL", "")
    submit_button = st.form_submit_button("Generate Print File")

if submit_button:
    if not reader_name or not audio_url:
        st.warning("Please enter both a name and a URL.")
    else:
        with st.spinner("Generating your custom bookplates..."):
            try:
                # Load the background image from your GitHub repo
                base_img = Image.open("image_66b396.jpg").convert("RGB")
            except FileNotFoundError:
                st.error("Error: Could not find 'image_66b396.jpg' in the repository.")
                st.stop()

            # Generate the QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=1,
            )
            qr.add_data(audio_url)
            qr.make(fit=True)
            
            # Create the QR code in a dark brown color to match your aesthetic
            qr_img = qr.make_image(fill_color="#4A3B32", back_color="white").convert("RGB")
            
            # Resize QR code to fit the white squares
            # Note: Adjust these dimensions (e.g., 350x350) based on your image resolution
            qr_size = (350, 350) 
            qr_img = qr_img.resize(qr_size)

            # Initialize ImageDraw for text overlay
            draw = ImageDraw.Draw(base_img)
            
            # Load a default font (For production, upload a TTF like Georgia.ttf to your repo)
            font = ImageFont.load_default()

            # Map out the 6 grid coordinates: {"qr": (X, Y), "text": (X, Y)}
            # These are placeholder coordinates. You must tweak them to perfectly align.
            positions = [
                {"qr": (1300, 500), "text": (500, 600)},   # Top Left
                {"qr": (3200, 500), "text": (2400, 600)},  # Top Right
                {"qr": (1300, 1600), "text": (500, 1700)}, # Middle Left
                {"qr": (3200, 1600), "text": (2400, 1700)},# Middle Right
                {"qr": (1300, 2700), "text": (500, 2800)}, # Bottom Left
                {"qr": (3200, 2700), "text": (2400, 2800)},# Bottom Right
            ]

            # Loop through all 6 positions and overlay the assets
            for pos in positions:
                base_img.paste(qr_img, pos["qr"])
                draw.text(pos["text"], reader_name, fill="#4A3B32", font=font)

            # Convert final image to a downloadable PDF in-memory
            pdf_bytes = io.BytesIO()
            base_img.save(pdf_bytes, format="PDF", resolution=300.0)
            pdf_bytes.seek(0)
            
            st.success("File generated successfully! Click below to download.")
            
            st.download_button(
                label="Download Ready-to-Print PDF",
                data=pdf_bytes,
                file_name="Storybound_Keepsakes_Printable.pdf",
                mime="application/pdf"
            )
