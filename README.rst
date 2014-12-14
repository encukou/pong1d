1D Pong for the Micropython Pyboard and a 144-LED WS2812 strip.


Push the button when the "ball" is in your goal area. Don't let it go
past the end of the strip, or you lose a point! When all of your 10
points are gone, game over.

When you push the button close to the ent of the strip, it will go faster,
making it harder for your opponent to react.

See the `youtube video`_ for a demo.

.. _youtube video: https://www.youtube.com/watch?v=fwyFTVJoppA

Software
--------

Requires the `micropython-ws2812`_ library with `my pull request`_ merged in.
Copy ``ws2812.py`` from there and ``main.py`` from here to your pyboard.

If you have more or fewer than 144 LEDs in your strip, adjust ``SIZE``
at the top of ``main.py``.

.. _micropython-ws2812: https://github.com/JanBednarik/micropython-ws2812

.. _my pull request: https://github.com/JanBednarik/micropython-ws2812/pull/1

Hardware
--------

Connect the LED strip to VIN (+), GND (-), and X8 (Data).
Connect a pushbutton between VIN and X4.

Operation
---------

Use the Pyboard's onboard switch to control one player's side;
the other player should use the pushbutton.


