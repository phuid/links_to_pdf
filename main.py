import qrcode
from fpdf import FPDF


f = open("input.txt", "r")


links = f.readlines()
images = []

for i, link in enumerate(links):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=0,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image()
    imgname = "images/test{}.png".format(i)
    img.save(imgname)
    images.append(imgname)

f.close()

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_font("Courier", size=12)
pdf.add_page()

xminus = 0

rows = 4
cols = 3

width = 50
height = 50

v_margin = 22
h_margin = 16

v_offset = 10
h_offset = 14

for x in range(0, len(links)):
    token = links[x][links[x].rfind("token=") + 6 :]
    pdf.image(
        images[x],
        x=(width + h_margin) * ((x - xminus) % cols) + h_offset,
        y=(height + v_margin) * ((x - xminus) // cols) + v_offset,
        w=width,
        h=height,
    )
    
    pdf.set_font("Arial", size=10)
    pdf.text(
        x=(width + h_margin) * ((x - xminus) % cols) + h_offset,
        y=(height + v_margin) * ((x - xminus) // cols) + 55 + v_offset,
        # txt=links[x][:links[x].rfind("?")],
        txt="majales.gyrec.cz/hlasovani.html"
    )
    pdf.text(
        x=(width + h_margin) * ((x - xminus) % cols) + h_offset,
        y=(height + v_margin) * ((x - xminus) // cols) + 60 + v_offset,
        txt="Unikátní kód: ",
    )
    pdf.set_font("Courier", size=12, style="B")
    pdf.text(
        x=(width + h_margin) * ((x - xminus) % cols) + 25 + h_offset,
        y=(height + v_margin) * ((x - xminus) // cols) + 60 + v_offset,
        txt=token,
    )
    if x % (rows * cols) == rows * cols - 1 and x != len(links) - 1:
        pdf.add_page()
        xminus += rows * cols

pdf.output("output.pdf", "F")
