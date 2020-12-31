from brother_ql.raster import BrotherQLRaster
from brother_ql.labels import Label, FormFactor, Color
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from create_pdf import create_printable
import firebase


def mm_to_dots(mm):
    return mm / 25.4 * 300


MODEL = "QL-810W"
BACKEND = "pyusb"
PRINTER = {
    "pyusb": "usb://0x04f9:0x209c",
    "network": "tcp://192.168.1.211"
}

LABEL_TYPE = FormFactor.ENDLESS
LABEL_SIZE_NAME = "62"
TAPE_SIZE = (62, 0)
MARGIN = 0.25 * 25.4
DOTS_TOTAL = (mm_to_dots(TAPE_SIZE[0]), 0)
DOTS_PRINTABLE = (mm_to_dots(DOTS_TOTAL[0] - MARGIN), 0)

orders = firebase.get_orders()
users = firebase.get_users()
app_data = firebase.get_app_data()

qlr = BrotherQLRaster(MODEL)
label = Label("1", (62, 0), LABEL_TYPE, DOTS_TOTAL, DOTS_PRINTABLE, mm_to_dots(MARGIN), color=Color.BLACK_RED_WHITE)
qlr.exception_on_warning = True

printables = []

for order in orders:
    printables += create_printable(order, users[order["uid"]], app_data)

instructions = convert(
    qlr=qlr,
    images=printables,
    label=LABEL_SIZE_NAME,
    rotate="0",
    threshold=95.0,    # Black and white threshold in percent.
    dither=False,
    compress=False,
    red=True,    # Only True if using Red/Black 62 mm label tape.
    dpi_600=False,
    lq=False,    # True for low quality.
    no_cut=False
)

send(instructions=instructions, printer_identifier=PRINTER[BACKEND], backend_identifier=BACKEND, blocking=True)
