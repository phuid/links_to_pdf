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

h_margin = 10
v_margin = 15

v_offset = 20
h_offset = 20

for x in range(0, len(links)):
    token = links[x][links[x].rfind("token=") + 6 :]
    pdf.image(
        images[x],
        x=(width + h_margin) * ((x - xminus) % cols) + h_offset,
        y=(height + v_margin) * ((x - xminus) // cols) + v_offset,
        w=width,
        h=height,
    )
    split = len(token) // 2
    pdf.text(
        x=(width + h_margin) * ((x - xminus) % cols) + h_offset,
        y=(height + v_margin) * ((x - xminus) // cols) + 55 + v_offset,
        txt=token[:split],
    )
    pdf.text(
        x=(width + h_margin) * ((x - xminus) % cols) + h_offset,
        y=(height + v_margin) * ((x - xminus) // cols) + 60 + v_offset,
        txt=token[split:],
    )
    if x % (rows * cols) == rows * cols - 1:
        pdf.add_page()
        xminus += rows * cols

pdf.output("output.pdf", "F")
