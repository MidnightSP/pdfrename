# SPDX-FileCopyrightText: 2020 Svetlana Pantelejeva
#
# SPDX-License-Identifier: MIT

import dateparser

from typing import Optional

from components import NameComponents
from utils import find_box_starting_with


def try_google(text_boxes, parent_logger) -> Optional[NameComponents]:
    logger = parent_logger.getChild("google")

    is_google = any("Google Commerce Limited\n" in box for box in text_boxes)
    if is_google:
        logger.debug("This is a Google invoice.")

        address_idx = text_boxes.index("Bill to\n")
        account_holder_name = text_boxes[address_idx + 1].strip()

        invoice_date_title_box = find_box_starting_with(text_boxes, "Invoice date\n")
        assert invoice_date_title_box
        invoice_date_idx = text_boxes.index(invoice_date_title_box) + 1

        invoice_date_str = text_boxes[invoice_date_idx]
        invoice_date = dateparser.parse(invoice_date_str, languages=["en"])
        assert invoice_date is not None

        return NameComponents(invoice_date, "Google", account_holder_name, "Invoice")
