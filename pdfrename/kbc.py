# SPDX-FileCopyrightText: 2020 Svetlana Pantelejeva
#
# SPDX-License-Identifier: MIT

import dateparser

from typing import Optional

from components import NameComponents
from utils import extract_account_holder_from_address


def try_kbc(text_boxes, parent_logger) -> Optional[NameComponents]:
    logger = parent_logger.getChild("kbc")

    is_kbc = any("ICONIE2D\n" in box for box in text_boxes)
    if is_kbc:
        logger.debug("Found KBC Ireland")

        account_holder_name = extract_account_holder_from_address(text_boxes[0])

        statement_date = dateparser.parse(text_boxes[1], languages=["en"])

        assert statement_date is not None

        return NameComponents(statement_date, "KBC", account_holder_name, "Statement")
