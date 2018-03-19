#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urwid
from datetime import datetime
import requests
import json

palette = [('titlebar', 'black', 'white'), ('refresh button',
                                            'dark green,bold', 'black'),
           ('quit button', 'dark red,bold', 'black'), ('getting quote',
                                                       'dark blue', 'black')]

now = datetime.now().strftime('%b %d, %I:%M:%S %p')

headerText = urwid.Text(f"BTC Price as of: {now}")

header = urwid.AttrMap(headerText, 'titlebar')
menu = urwid.Text(
    ['Press (', ('refresh button', 'enter'), ') to get a new quote.'])

quoteText = urwid.Text('Press (enter) to get a new quote.')
quoteFiller = urwid.Filler(quoteText, valign='top', top=1, bottom=1)
vPadding = urwid.Padding(quoteFiller, left=1, right=1)
quoteBox = urwid.LineBox(vPadding)

layout = urwid.Frame(header=header, body=quoteBox, footer=menu)


def getQuote() -> str:
    url = 'https://api.coindesk.com/v1/bpi/currentprice/usd.json'
    response = requests.get(url)
    jsonOut = json.loads(response.text)
    out = jsonOut['bpi']['USD']['rate']
    return out


def handleInput(key):
    if key == 'enter':
        quoteBox.base_widget.set_text(('getting quote',
                                       'Getting new quote ...'))
        now = datetime.now().strftime('%b %d, %I:%M:%S %p ')
        main_loop.draw_screen()
        header.base_widget.set_text(f"BTC Price as of: {now}")
        quoteBox.base_widget.set_text(getQuote())
    if key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()


main_loop = urwid.MainLoop(layout, palette, unhandled_input=handleInput)

main_loop.run()
